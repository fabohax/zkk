from binius.binary_fields import BinaryFieldElement

def log2(x):
    return x.bit_length() - 1

def pack_vector(vector, packing_factor):
    packed = []
    for i in range(0, len(vector), packing_factor):
        value = sum(v.value << j for j, v in enumerate(vector[i:i + packing_factor]))
        packed.append(value)
    return packed

def evaluation_tensor_product(point):
    """
    Generate a tensor product for evaluations. Each element in the
    product is based on the values in the given evaluation point.
    """
    n = len(point)
    if (1 << n) != len(point):
        raise ValueError("The length of the evaluation point does not match the expected power of 2.")

    product = [1]  # Start with the identity element for multiplication
    for i in range(n):
        product = [
            x * (1 - point[i].value) for x in product
        ] + [
            x * point[i].value for x in product
        ]

    # Return only the portion corresponding to `row_count`
    return product[: (1 << n)]

def multilinear_poly_eval(evaluations, evaluation_point):
    """
    Evaluate multilinear polynomials at the given point.
    """
    result = evaluations[0]
    n = len(evaluation_point)
    for i in range(1, 1 << n):
        weight = 1
        for j in range(n):
            if (i >> j) & 1:
                weight *= evaluation_point[j].value
            else:
                weight *= (1 - evaluation_point[j].value)
        result += evaluations[i] * weight
    return result
