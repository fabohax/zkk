import hashlib
from typing import List


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class MerkleTree:
    def __init__(self, leaves: List[str]):
        self.leaves = [sha256(leaf.encode()) for leaf in leaves]
        self.tree = []
        self.root = self.build_tree(self.leaves)

    def build_tree(self, nodes: List[str]) -> str:
        """Constructs the Merkle Tree and returns the Merkle root."""
        if len(nodes) == 1:
            return nodes[0]
        
        new_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else left  # Duplicate last node if odd number
            new_level.append(sha256((left + right).encode()))
        
        self.tree.append(new_level)
        return self.build_tree(new_level)

    def get_root(self) -> str:
        """Returns the Merkle Root."""
        return self.root

    def get_proof(self, leaf: str) -> List[str]:
        """Generates a Merkle proof for a given leaf."""
        leaf_hash = sha256(leaf.encode())
        proof = []
        level = self.leaves
        
        while len(level) > 1:
            new_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i + 1] if i + 1 < len(level) else left
                combined = sha256((left + right).encode())
                
                if leaf_hash == left:
                    proof.append(right)
                elif leaf_hash == right:
                    proof.append(left)
                
                new_level.append(combined)
            
            level = new_level
            if leaf_hash in level:
                break
        
        return proof

    def verify_proof(self, leaf: str, proof: List[str], root: str) -> bool:
        """Verifies a given Merkle proof."""
        leaf_hash = sha256(leaf.encode())
        computed_hash = leaf_hash
        
        for sibling in proof:
            combined = (computed_hash + sibling).encode()
            computed_hash = sha256(combined)
        
        return computed_hash == root


# Example Usage
if __name__ == "__main__":
    leaves = ["tx1", "tx2", "tx3", "tx4"]
    tree = MerkleTree(leaves)
    root = tree.get_root()
    print("Merkle Root:", root)
    
    leaf = "tx2"
    proof = tree.get_proof(leaf)
    print("Merkle Proof for", leaf, ":", proof)
    
    valid = tree.verify_proof(leaf, proof, root)
    print("Proof Valid:", valid)
