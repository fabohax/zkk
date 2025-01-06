#!/bin/bash

# Exit on any error
set -e

# Define variables
VENV_DIR="venv"

# Step 1: Check Python version
REQUIRED_PYTHON="3.8"
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
if [[ "$PYTHON_VERSION" < "$REQUIRED_PYTHON" ]]; then
    echo "Python $REQUIRED_PYTHON or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "Python version check passed: $PYTHON_VERSION"

# Step 2: Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Step 3: Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Step 4: Upgrade pip and setuptools
echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools

# Step 5: Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 6: Install project in editable mode (if setup.py exists)
if [ -f "setup.py" ]; then
    echo "Installing project in editable mode..."
    pip install -e .
else
    echo "setup.py not found. Skipping project installation."
fi

# Step 7: Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Environment setup complete!"
