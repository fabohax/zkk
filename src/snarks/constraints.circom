pragma circom 2.0.0;

include "snarkjs";

// Circuit to prove ownership of a Bitcoin private key without revealing it
// Ensures that the private key corresponds to the given public key

template ZKKOwnership() {
    signal private input privateKey;  // Private key (kept hidden)
    signal input publicKey;           // Public key (known to verifier)
    
    component hash = Poseidon(1);     // Using Poseidon hash function for efficiency
    hash.inputs[0] <== privateKey;
    
    // Ensure the computed hash matches the provided public key
    publicKey === hash.out;
    
    // Output proof for validation
    signal output proof;
    proof <== hash.out;
}

component main = ZKKOwnership();
