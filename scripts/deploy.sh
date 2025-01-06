#!/bin/bash

# Exit on any error
set -e

# Define variables
VENV_DIR="venv"
PROJECT_NAME="zkk_project"

# Step 1: Create and activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Step 2: Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip setuptools
pip install -r requirements.txt

# Step 3: Run tests
if [ -d "tests" ]; then
    echo "Running tests..."
    pytest tests
else
    echo "No tests directory found, skipping tests."
fi

# Step 4: Build the package
if [ -f "setup.py" ]; then
    echo "Building package..."
    python setup.py sdist bdist_wheel
else
    echo "setup.py not found. Skipping build."
fi

# Step 5: Deploy the package (example: uploading to PyPI)
if [ "$1" == "release" ]; then
    echo "Deploying package to PyPI..."
    if [ ! -f "$HOME/.pypirc" ]; then
        echo "~/.pypirc file not found. Please configure it for PyPI deployment."
        exit 1
    fi
    twine upload dist/*
else
    echo "Skipping PyPI deployment. Use './deploy.sh release' to deploy."
fi

# Step 6: Cleanup
echo "Deactivating virtual environment..."
deactivate

echo "Deployment complete!"
