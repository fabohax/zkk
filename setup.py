from setuptools import setup, find_packages

setup(
    name="zkk",
    version="1.0.0",
    description="Zero-Knowledge Key (ZKK): A Python-based implementation of zero-knowledge proofs for Bitcoin private key validation using PySNARK.",
    author="fabohax",
    author_email="40230@pm.me",
    url="https://github.com/fabohax/zkk",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "bit", 
        "qrcode==7.4",
        "pysnark",  
        "numpy>=1.21.4",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)