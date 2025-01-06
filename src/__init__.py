# src/__init__.py

__version__ = "1.0.0"

# Expose modules for easier imports
default_modules = [
    "binius.proof",
    "binius.binary_fields",
    "binius.utils",
    "binius.merkle",
    "bitcoin.key_utils",
    "qr.generate_qr",
]

print(f"Loaded ZKK modules: {', '.join(default_modules)}")
