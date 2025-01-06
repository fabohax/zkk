# ZKK: Zero-Knowledge Key

ZKK is a proof-of-concept project demonstrating the use of **Zero-Knowledge Proofs (ZKP)** to validate a Bitcoin private key without exposing its value. The project generates a ZKP proving that a given private key corresponds to a derived public key and encodes the proof in a QR code for easy sharing and validation.

## Features

- Validate Bitcoin private keys.
- Derive public keys and addresses from private keys.
- Generate Zero-Knowledge Proofs (ZKP) using `binius`.
- Encode ZKP into a QR code for secure sharing.
- Display and save QR codes as SVG images.

## Prerequisites

1. **Python 3.8 or later**: Ensure you have Python installed.
2. **Dependencies**:
   - `bitcoinlib`: For Bitcoin key derivation.
   - `qrcode`: For QR code generation.
   - `binius`: For ZKP generation and verification.

Install dependencies using:
```bash
pip install bitcoinlib qrcode binius
```

## Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/fabohax/zkk.git
cd zkk
```

## Project Structure

```
zkk_project/
├── bin/
│   └── cli.py                 # CLI script for ZKP generation and verification
├── src/
│   ├── binius/                # Binius proof-related code
│   │   ├── proof.py           # Proof generation and verification logic
│   │   ├── binary_fields.py   # Binary field operations
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
   - Using `binius`, the private key is input as a binary evaluation.
   - The proof is generated based on a securely chosen evaluation point.
   - The output is a ZKP that can be validated without exposing the private key.

3. **Encode in QR Code**:
   - The generated ZKP is serialized and encoded into a QR code for sharing.
   - The QR code is saved as an SVG image.

## Usage

### 1. Run the Script
Generate a proof and QR code for a given Bitcoin private key:
```bash
python bin/cli.py <BitcoinPrivateKey>
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

**Generated QR Code (in Terminal):**
```
█████████████████████████████
████ ▄▄▄▄▄ █▄▀█▄▄▄ ▄▄▄▄▄ ████
████ █   █ █▀▄ ▄▄▄ █   █ ████
████ █▄▄▄█ █▄▀▄▀▄█ █▄▄▄█ ████
████▄▄▄▄▄▄▄█▄█▄█▄█▄▄▄▄▄▄▄████
████ ▄▄▄▄▄ ██▄▄ ▀▄▄ ▄█▄█▄████
████ █   █ █ ▀▀▄█▄▀█▀▄▀▄ ████
████ █▄▄▄█ █ ▀▄█▄▀ ▄█▀ ▄█████
████▄▄▄▄▄▄▄█▄█▄█▄▄█▄▄▄██▄████
████ ▄▄▄▄▄ ██ ▀█▄ ▄▄█ ▄▀█████
████ █   █ █▄▄▄█ ▀█ ▀▄██▀████
████ █▄▄▄█ █ ▄▄▄▄ ▀ ▄▄▄▄█████
████▄▄▄▄▄▄▄█▄▄▄▄▄█▄█▄▄▄▄▄████
█████████████████████████████
```

### 3. Verify the Proof
Run the verification script to confirm proof validity:
```bash
python bin/cli.py --verify <path_to_proof_file>
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

Made with ❤️ 

