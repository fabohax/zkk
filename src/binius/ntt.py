from binius.utils import pack_vector
from binius.binary_fields import BinaryFieldElement

def extend_row_of_bits(row, expansion_factor=8, packing_factor=16):
    """
    Extend a row of bits using a Reed-Solomon-like code. Each slice of
    `packing_factor` bits is treated as a single field element, and then
    expanded using the given expansion factor.
    """
    if len(row) % packing_factor != 0:
        raise ValueError("Row length must be a multiple of packing factor")

    # Pack bits into field elements
    packed_row = pack_vector(row, packing_factor)

    # Extend each packed element by expansion factor
    extended_row = []
    for element in packed_row:
        for i in range(expansion_factor):
            extended_row.append(BinaryFieldElement(element ^ i))

    return extended_row
