import sys
import os
import argparse
import json
import qrcode

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.bitcoin.key_utils import validate_private_key_raw, derive_public_key, derive_address
from src.snarks.proof import generate_zk_proof, verify_zk_proof

def generate_proof(private_key):
    print("Validating and deriving public key and address...")
    public_key = derive_public_key(private_key)
    address = derive_address(private_key)
    print(f"Public Key: {public_key}")
    print(f"Address: {address}")

    print("Generating ZKP...")
    proof = generate_zk_proof(private_key, public_key)
    proof_data = {
        "proof": proof,
        "public_key": public_key,
        "address": address
    }
    
    qr = qrcode.QRCode()
    qr.add_data(json.dumps(proof_data))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"zkp_qr_{public_key[:8]}.svg")
    print("ZKP Generated Successfully.")
    print(f"QR Code saved as zkp_qr_{public_key[:8]}.svg")

def verify_proof(proof_path):
    with open(proof_path, "r") as f:
        proof_data = json.load(f)
    
    print("Verifying ZKP...")
    is_valid = verify_zk_proof(proof_data["proof"], proof_data["public_key"])
    
    if is_valid:
        print("Proof is valid!")
    else:
        print("Proof verification failed.")

def main():
    parser = argparse.ArgumentParser(description="ZKK CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    gen_parser = subparsers.add_parser("generate", help="Generate a zk-SNARK proof and QR code")
    gen_parser.add_argument("private_key", type=str, help="Bitcoin private key")

    verify_parser = subparsers.add_parser("verify", help="Verify a zk-SNARK proof")
    verify_parser.add_argument("proof_path", type=str, help="Path to the proof JSON file")

    args = parser.parse_args()

    if args.command == "generate":
        try:
            validate_private_key_raw(args.private_key)
            generate_proof(args.private_key)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "verify":
        verify_proof(args.proof_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
