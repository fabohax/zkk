# 🔑 ZKK: Zero-Knowledge Key

ZKK is a proof-of-concept project demonstrating the use of **Zero-Knowledge Proofs (ZKP)** to validate a Bitcoin private key without exposing its value. The project generates a ZKP proving that a given private key corresponds to a derived public key and encodes the proof in a QR code for easy sharing and validation.

## Features

- Validate Bitcoin private keys.
- Derive public keys and addresses from private keys.
- Generate Zero-Knowledge Proofs (ZKP) using `zk-SNARKs`.
- Encode ZKP into a QR code for secure sharing.
- Display and save QR codes as SVG images.

## Prerequisites

1. **Python 3.8 or later**: Ensure you have Python installed.
2. **Environment Setup**: Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Dependencies**:
   - `bitcoinlib`: For Bitcoin key derivation.
   - `qrcode`: For QR code generation.
   - `snarkjs`: For zk-SNARK proof generation.

Install dependencies using:
```bash
pip install bitcoinlib qrcode snarkjs
```

## Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/fabohax/zkk.git
cd zkk
```

## Use Cases

ZKK can be used in scenarios where you want to prove knowledge or ownership of a Bitcoin private key without revealing the key itself. Example use cases include:

- **Anonymous Authentication:** Prove you control a Bitcoin address (or cryptographic identity) without revealing your public key or address. Useful for privacy-preserving logins or gated access.
- **Private Ownership Proof:** Show you own a specific Bitcoin address to a third party (e.g., for KYC, asset verification, or escrow) without exposing your private key or even your public key.
- **Selective Disclosure:** Prove you control one address from a set (e.g., “I own one of these addresses”) without revealing which one, useful for anonymous group membership or voting.
- **On-chain Privacy Protocols:** Integrate with smart contracts or privacy-focused blockchains to prove transaction validity or ownership without leaking sensitive information.
- **Credential Systems:** Use as a building block for decentralized identity, where you prove attributes (like age, membership, or asset ownership) without revealing your identity.
- **Secure Messaging or Signing:** Prove you can decrypt or sign messages without revealing your key, enabling secure, private communication channels.

## Project Structure

```
zkk/
├── bin/
│   └── cli.py                 # CLI script for ZKP generation and verification
├── src/
│   ├── snarks/                # zk-SNARK proof-related code
│   │   ├── proof.py           # Proof generation and verification logic
│   │   ├── constraints.circom # Circom circuit for zk-SNARKs
│   │   ├── utils.py           # Utility functions for evaluation
│   │   └── merkle.py          # Merkle tree implementation
│   ├── bitcoin/
│   │   └── key_utils.py       # Functions for key derivation and validation
│   └── qr/
│       └── generate_qr.py     # QR code generation utilities
├── tests/                     # Unit and integration tests
├── examples/                  # Example scripts for usage
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## How It Works

1. **Validate and Derive Public Key**:
   - The script validates a given Bitcoin private key.
   - It derives the corresponding public key and Bitcoin address.

2. **Generate ZKP**:
   - Using `zk-SNARKs`, the private key is input into a Circom circuit.
   - The proof is generated via `snarkjs` based on the circuit constraints.
   - The output is a ZKP that can be validated without exposing the private key.

3. **Encode in QR Code**:
   - The generated ZKP is serialized and encoded into a QR code for sharing.
   - The QR code is saved as an SVG image.

## Usage

### 1. Run the Script
Generate a proof and QR code for a given Bitcoin private key:
```bash
python bin/cli.py generate <BitcoinPrivateKey>
```

### 2. Example Output
**Console Output:**
```
Validating and deriving public key...
Public Key: 02c2977508521f90683cae95a21824b89e5ee4604869c5e383cb85cdd4c2148c00
Address: 19cf4bxogLyzo3yCEedyLq3nwdy6r43RsF
Generating ZKP...
ZKP Generated Successfully.
QR Code saved as zkp_qr.svg
```

### 3. Verify the Proof
Run the verification script to confirm proof validity:
```bash
python bin/cli.py --verify <path_to_proof_file>
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

Open Source Code Made With ❤️

Consider to donate to 

```bash
bc1p0saw6z028y7h6eag3w6hx5an6mk5ta8qk7wx2d3gtqtrty243uvqvjzvew
```