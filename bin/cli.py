import sys
import os
import argparse
from bitcoin.key_utils import derive_public_key, derive_address
from binius.proof import packed_binius_proof, verify_packed_binius_proof
from binius.binary_fields import BinaryFieldElement
from qr.generate_qr import generate_qr_code

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

# Function to generate a proof and QR code
def generate_proof(private_key_raw):
    print("Deriving public key and address...")
    public_key = derive_public_key(private_key_raw)
    address = derive_address(private_key_raw)

    print(f"Public Key: {public_key}")
    print(f"Address: {address}")

    # Convert the raw private key to binary evaluations
    evaluations = [BinaryFieldElement(int(bit)) for bit in bin(int(private_key_raw, 16))[2:]]

    # Generate a dummy evaluation point (replace with a secure point in production)
    evaluation_point = [BinaryFieldElement(0), BinaryFieldElement(1)]

    print("Generating Zero-Knowledge Proof...")
    proof = packed_binius_proof(evaluations, evaluation_point)

    print("Proof generated successfully.")
    generate_qr_code(str(proof), "zkp_qr.svg")
    print("QR Code saved as zkp_qr.svg")

# Function to verify a proof
def verify_proof(proof):
    print("Verifying proof...")
    is_valid = verify_packed_binius_proof(proof)
    if is_valid:
        print("Proof verification successful.")
    else:
        print("Proof verification failed.")

# Main CLI function
def main():
    parser = argparse.ArgumentParser(description="ZKK: Zero-Knowledge Key CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: Generate Proof
    generate_parser = subparsers.add_parser("generate", help="Generate a Zero-Knowledge Proof and QR code")
    generate_parser.add_argument("private_key_raw", help="Raw Bitcoin private key in hexadecimal format")

    # Subcommand: Verify Proof
    verify_parser = subparsers.add_parser("verify", help="Verify a Zero-Knowledge Proof")
    verify_parser.add_argument("proof_file", help="Path to the proof file to verify")

    args = parser.parse_args()

    if args.command == "generate":
        generate_proof(args.private_key_raw)
    elif args.command == "verify":
        with open(args.proof_file, "r") as f:
            proof = eval(f.read())  # Replace eval with safer deserialization in production
        verify_proof(proof)

if __name__ == "__main__":
    main()
