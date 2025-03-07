import hashlib
import os
import json

def sha256(data: str) -> str:
    """Computes SHA-256 hash of a given string."""
    return hashlib.sha256(data.encode()).hexdigest()


def save_json(data: dict, filename: str):
    """Saves a dictionary as a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_json(filename: str) -> dict:
    """Loads a JSON file into a dictionary."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)


def generate_nonce() -> str:
    """Generates a cryptographic nonce."""
    return os.urandom(16).hex()


if __name__ == "__main__":
    # Example usage
    print("SHA-256 of 'test':", sha256("test"))
    print("Generated nonce:", generate_nonce())