# ZKK: Zero-Knowledge Key

ZKK is a proof-of-concept project demonstrating the use of **Zero-Knowledge Proofs (ZKP)** to validate a Bitcoin private key without exposing its value. The project generates a ZKP proving that a given private key corresponds to a derived public key and encodes the proof in a QR code for easy sharing and validation.

## Features

- Validate Bitcoin private keys (in WIF format).
- Derive public keys and addresses from private keys.
- Generate Zero-Knowledge Proofs (ZKP) using `snarkjs`.
- Encode ZKP into a QR code for secure sharing.
- Display and save QR codes as SVG images.

## Prerequisites

1. **Node.js**: Ensure you have Node.js installed (version 14 or later).
2. **Circom**: Install Circom for circuit compilation.
3. **snarkjs**: Install `snarkjs` for ZKP setup and proof generation.
4. **npm packages**:
   - `bitcoinjs-lib`
   - `commander`
   - `qrcode`
   - `snarkjs`
   - `bip39` (if mnemonic support is needed)
   - `wif`

Install dependencies using:
```bash
npm install bitcoinjs-lib commander qrcode snarkjs wif
```

## Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/fabohax/zkk.git
cd zkk
```

## Project Structure

```
.
├── privateKeyVerification.circom  # The ZKP circuit definition
├── privateKeyVerification_js/     # Compiled WASM file and metadata
├── zkk.js                         # Main script for ZKP generation
├── README.md                      # Project documentation
└── package.json                   # Node.js project configuration
```

## How It Works

1. **Validate and Derive Public Key**:
   - The script validates a given Bitcoin private key (in WIF format).
   - It derives the corresponding public key and Bitcoin address.

2. **Generate ZKP**:
   - Using `snarkjs`, the private key is input into a Circom circuit (`privateKeyVerification.circom`).
   - The circuit verifies that the private key corresponds to the public key.
   - The output is a ZKP that can be validated without exposing the private key.

3. **Encode in QR Code**:
   - The generated ZKP is serialized and encoded into a QR code for sharing.
   - The QR code is displayed in the terminal and saved as an SVG image.

## Usage

### 1. Compile the Circuit
Ensure `privateKeyVerification.circom` is correctly defined. Then compile:
```bash
circom privateKeyVerification.circom --r1cs --wasm --sym
```

### 2. Perform Trusted Setup
Run the trusted setup for zk-SNARKs:
```bash
snarkjs groth16 setup privateKeyVerification.r1cs pot12_final.ptau circuit_final.zkey
```
Export the verification key:
```bash
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json
```

### 3. Generate ZKP
Run the script to generate the ZKP and encode it in a QR code:
```bash
node zkk.js <BitcoinPrivateKeyWIF>
```

## Example Output

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

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

Made with ❤️ by fabohax