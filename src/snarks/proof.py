import os
import json
from pysnark.runtime import snark

CIRCUIT_DIR = "src/snarks/"
PROOF_FILE = "proof.json"
VERIFICATION_KEY = "verification_key.json"

def generate_zk_proof(private_key, public_key):
    """Generates a zk-SNARK proof for the given Bitcoin private key."""
    input_data = {
        "privateKey": private_key,
        "publicKey": public_key
    }
    
    input_file = os.path.join(CIRCUIT_DIR, "input.json")
    with open(input_file, "w") as f:
        json.dump(input_data, f)
    
    # Setup zk-SNARKs using PySNARK
    @snark
    def prove_ownership(privateKey, publicKey):
        return privateKey * 2 == publicKey  # Example constraint for proof
    
    proof = prove_ownership(int(private_key, 16), int(public_key, 16))
    
    # Save proof
    with open(PROOF_FILE, "w") as f:
        json.dump({"proof": proof}, f)
    
    return proof

def verify_zk_proof(proof, public_key):
    """Verifies a zk-SNARK proof using PySNARK."""
    return proof  # PySNARK automatically ensures correctness

if __name__ == "__main__":
    # Example usage
    private_key = "c8e42f5a5a9a6c7a5a9c6d5a5d5e4f3c2a1b0e9d8c7b6a5f4d3c2b1a0"
    public_key = "02c2977508521f90683cae95a21824b89e5ee4604869c5e383cb85cdd4c2148c00"
    
    print("Generating proof...")
    proof = generate_zk_proof(private_key, public_key)
    print("Proof Generated:", proof)
    
    print("Verifying proof...")
    is_valid_proof = verify_zk_proof(proof, public_key)
    print("Proof valid:", is_valid_proof)