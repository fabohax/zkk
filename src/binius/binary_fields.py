class BinaryFieldElement:
    def __init__(self, value):
        self.value = value & 1  # Binary field: 0 or 1

    def __add__(self, other):
        return BinaryFieldElement(self.value ^ other.value)

    def __mul__(self, other):
        return BinaryFieldElement(self.value & other.value)

    def __repr__(self):
        return str(self.value)
