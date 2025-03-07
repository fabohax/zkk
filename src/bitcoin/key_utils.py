from bit import Key

# Utility functions for Bitcoin key derivation and validation
def validate_private_key_raw(private_key_raw):
    """Validate and decode a raw Bitcoin private key in WIF format."""
    try:
        key = Key(private_key_raw)  # Corrected to match `bit` library usage
        return key
    except Exception as e:
        raise ValueError(f"Invalid raw private key: {str(e)}")

def derive_public_key(private_key_raw):
    """Derive the public key from a raw private key."""
    key = validate_private_key_raw(private_key_raw)
    return key.public_key.hex()  # Ensure correct public key format

def derive_address(private_key_raw):
    """Derive the Bitcoin address from a raw private key."""
    key = validate_private_key_raw(private_key_raw)
    return key.address

# Remove unused imports from the older implementation
__all__ = [
    "validate_private_key_raw",
    "derive_public_key",
    "derive_address",
]
