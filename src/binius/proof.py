from binius.utils import log2, evaluation_tensor_product, multilinear_poly_eval
from binius.binary_fields import BinaryFieldElement
from binius.merkle import merkelize, get_root, get_branch, verify_branch
from binius.ntt import extend_row_of_bits

EXPANSION_FACTOR = 8
NUM_CHALLENGES = 32
PACKING_FACTOR = 16

def choose_row_length_and_count(log_evaluation_count):
    log_row_length = (log_evaluation_count + 2) // 2
    log_row_count = log_evaluation_count - log_row_length
    row_length = 1 << log_row_length
    row_count = 1 << log_row_count
    return log_row_length, log_row_count, row_length, row_count

def packed_binius_proof(evaluations, evaluation_point):
    # Pad evaluations to the nearest power of 2
    original_length = len(evaluations)
    next_power_of_2 = 1 << (original_length - 1).bit_length()
    evaluations += [BinaryFieldElement(0)] * (next_power_of_2 - original_length)

    print(f"Padded evaluations from {original_length} to {len(evaluations)}")

    # Rearrange evaluations into a row_length * row_count grid
    log_row_length, log_row_count, row_length, row_count = \
        choose_row_length_and_count(log2(len(evaluations)))
    rows = [
        evaluations[i:i + row_length]
        for i in range(0, len(evaluations), row_length)
    ]

    # Check dimensions
    if len(rows) != row_count:
        raise ValueError(f"Row count mismatch: Expected {row_count}, got {len(rows)}")

    # Extend each row using a Reed-Solomon code
    extended_rows = [extend_row_of_bits(row) for row in rows]
    extended_row_length = row_length * EXPANSION_FACTOR // PACKING_FACTOR

    # Compute t_prime, a linear combination of the rows
    if len(evaluation_point) < log_row_length:
        evaluation_point.extend([BinaryFieldElement(0)] * (log_row_length - len(evaluation_point)))
    row_combination = evaluation_tensor_product(evaluation_point[:log_row_length])
    if len(row_combination) != row_count:
        raise ValueError(f"Row combination mismatch: Expected {row_count}, got {len(row_combination)}")

    t_prime = [
        sum(
            row_combination[i] * rows[i][j] for i in range(row_count)
        ) for j in range(row_length)
    ]

    # Pack columns into a Merkle tree, to commit to them
    columns = [
        [row[j] for row in extended_rows]
        for j in range(extended_row_length)
    ]
    bytes_per_element = PACKING_FACTOR // 8
    packed_columns = [
        b''.join(x.to_bytes(bytes_per_element, 'little') for x in col)
        for col in columns
    ]
    merkle_tree = merkelize(packed_columns)
    root = get_root(merkle_tree)

    # Challenge in a few positions, to get branches
    challenges = [
        int.from_bytes(hash(root + bytes([i])), 'little') % extended_row_length
        for i in range(NUM_CHALLENGES)
    ]
    return {
        'root': root,
        'evaluation_point': evaluation_point,
        'eval': multilinear_poly_eval(evaluations, evaluation_point),
        't_prime': t_prime,
        'columns': [columns[c] for c in challenges],
        'branches': [get_branch(merkle_tree, c) for c in challenges],
    }

def verify_packed_binius_proof(proof):
    columns, evaluation_point, value, t_prime, root, branches = (
        proof['columns'],
        proof['evaluation_point'],
        proof['eval'],
        proof['t_prime'],
        proof['root'],
        proof['branches'],
    )

    # Compute the row length and row count of the grid. Should output same
    # numbers as what prover gave
    log_row_length, log_row_count, row_length, row_count = \
        choose_row_length_and_count(len(evaluation_point))
    extended_row_length = row_length * EXPANSION_FACTOR // PACKING_FACTOR

    # Compute challenges. Should output the same as what prover computed
    challenges = [
        int.from_bytes(hash(root + bytes([i])), 'little') % extended_row_length
        for i in range(NUM_CHALLENGES)
    ]

    # Verify the correctness of the Merkle branches
    bytes_per_element = PACKING_FACTOR // 8
    for challenge, branch, col in zip(challenges, branches, columns):
        packed_column = \
            b''.join(x.to_bytes(bytes_per_element, 'little') for x in col)
        print(f"Verifying Merkle branch for column {challenge}")
        assert verify_branch(root, challenge, packed_column, branch)

    # Use the same Reed-Solomon code that the prover used to extend the rows,
    # but to extend t_prime. We do this separately for each bit of t_prime
    t_prime_bit_length = max(x.bit_length() for x in evaluation_point)
    extended_slices = [
        extend_row_of_bits([unpack_bit(v, i) for v in t_prime])
        for i in range(t_prime_bit_length)
    ]

    # Here, we take advantage of the linearity of the code. A linear combination
    # of the Reed-Solomon extension gives the same result as an extension of the
    # linear combination.
    row_combination = \
        evaluation_tensor_product(evaluation_point[:log_row_length])
    for column, challenge in zip(columns, challenges):
        # Each extended row, at the column we're querying, contains a field
        # element `PACKING_FACTOR` bits wide. We treat each bit separately
        for b in range(PACKING_FACTOR):
            # We apply the same linear combination to that sub-column of bits
            # that the prover applied to generate t_prime
            computed_tprime = sum(
                [
                    row_combination[i] * unpack_bit(column[i], b)
                    for i in range(row_count)
                ],
                BinaryFieldElement(0)
            )
            expected_tprime = pack_vector([
                unpack_bit(_slice[challenge], b)
                for _slice in extended_slices
            ], 128)[0]
            assert expected_tprime == computed_tprime
    print("T_prime matches Merkle branches")

    # Take the right linear combination of elements *within* t_prime to
    # extract the evaluation of the original multilinear polynomial at
    # the desired point
    col_combination = \
        evaluation_tensor_product(evaluation_point[:log_row_length])
    computed_eval = sum(
        [t_prime[i] * col_combination[i] for i in range(row_length)],
        BinaryFieldElement(0)
    )
    print(f"Testing evaluation: expected {value} computed {computed_eval}")
    assert computed_eval == value
    return True