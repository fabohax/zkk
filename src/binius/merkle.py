import hashlib

def hash(data):
    """Hash data using SHA-256."""
    return hashlib.sha256(data).digest()

def merkelize(data):
    """Build a Merkle tree from the data."""
    if len(data) == 0:
        raise ValueError("Data must not be empty")

    tree = [hash(item) for item in data]

    while len(tree) > 1:
        next_level = []
        for i in range(0, len(tree), 2):
            if i + 1 < len(tree):
                combined = tree[i] + tree[i + 1]
            else:
                combined = tree[i] + tree[i]  # Duplicate the last element if odd number of nodes
            next_level.append(hash(combined))
        tree = next_level

    return tree

def get_root(tree):
    """Get the root of the Merkle tree."""
    if len(tree) == 0:
        raise ValueError("Tree is empty")
    return tree[0]

def get_branch(tree, index):
    """Retrieve a branch (proof) for a specific index."""
    branch = []
    level = [hash(item) for item in tree]

    while len(level) > 1:
        if index % 2 == 0:  # Left child
            sibling_index = index + 1 if index + 1 < len(level) else index
        else:  # Right child
            sibling_index = index - 1
        branch.append(level[sibling_index])
        index //= 2

        # Move to the next level of the tree
        next_level = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                combined = level[i] + level[i + 1]
            else:
                combined = level[i] + level[i]  # Duplicate the last element
            next_level.append(hash(combined))
        level = next_level

    return branch

def verify_branch(root, index, value, branch):
    """Verify that the value at index is valid with respect to the root."""
    current_hash = hash(value)
    for sibling_hash in branch:
        if index % 2 == 0:  # Left child
            current_hash = hash(current_hash + sibling_hash)
        else:  # Right child
            current_hash = hash(sibling_hash + current_hash)
        index //= 2

    return current_hash == root
