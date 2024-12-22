#!/usr/bin/env node

import { program } from "commander";
import QRCode from "qrcode";
import * as bitcoin from "bitcoinjs-lib";
import * as snarkjs from "snarkjs";
import fs from "fs";

// Validate and derive public key from Bitcoin private key
function derivePublicKeyFromPrivateKey(privateKeyWIF) {
    try {
        // Decode WIF and derive the key pair
        const keyPair = bitcoin.ECPair.fromWIF(privateKeyWIF);
        const publicKey = keyPair.publicKey.toString('hex');
        const address = bitcoin.payments.p2pkh({ pubkey: keyPair.publicKey }).address;

        console.log('Public Key:', publicKey);
        console.log('Address:', address);
    } catch (error) {
        console.error('Invalid WIF key:', error.message);
    }
}

// Generate ZKP using snarkjs
async function generateZKP(privateKey, publicKey) {
    const wasmPath = "./privateKeyVerification_js/privateKeyVerification.wasm";
    const zkeyPath = "./circuit_final.zkey";

    const input = {
        privateKey: privateKey, // Private key for proof
        publicKey: publicKey   // Public key for verification
    };

    const { proof, publicSignals } = await snarkjs.groth16.fullProve(input, wasmPath, zkeyPath);

    return JSON.stringify({ proof, publicSignals });
}

// Generate QR code
async function generateQRCode(data, outputSVG = "zkp_qr.svg") {
    // Print QR code in terminal
    console.log("QR Code:");
    console.log(await QRCode.toString(data, { type: "terminal" }));

    // Save QR code as SVG
    await QRCode.toFile(outputSVG, data, { type: "svg" });
    console.log(`QR Code saved as ${outputSVG}`);
}

// Main function for CLI
async function main(privateKeyWIF) {
    try {
        console.log("Validating and deriving public key...");
        const publicKey = derivePublicKeyFromPrivateKey(privateKeyWIF);
        console.log("Public Key Derived:", publicKey);

        console.log("Generating ZKP...");
        const zkp = await generateZKP(privateKeyWIF, publicKey);
        console.log("ZKP Generated:", zkp);

        console.log("Generating QR Code...");
        await generateQRCode(zkp);
        console.log("Process complete!");
    } catch (error) {
        console.error("Error:", error.message);
    }
}

// CLI interface
program
    .argument("<privateKeyWIF>", "Bitcoin private key in WIF format")
    .action(main);

program.parse(process.argv);
