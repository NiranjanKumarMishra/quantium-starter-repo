#!/bin/bash

# This script activates the Python virtual environment and runs the pytest suite.
# It returns an exit code of 0 for success or 1 for failure.

# Define the path to your virtual environment
VENV_PATH="./venv"

# --- Step 1: Activate the project virtual environment ---
# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH."
    echo "Please ensure you have created and installed dependencies in your venv."
    exit 1
fi

# Activate the virtual environment based on OS
if [ -f "$VENV_PATH/bin/activate" ]; then # For Linux/macOS
    source "$VENV_PATH/bin/activate"
    echo "Virtual environment activated (Linux/macOS)."
elif [ -f "$VENV_PATH/Scripts/activate" ]; then # For Windows (Git Bash/WSL)
    source "$VENV_PATH/Scripts/activate"
    echo "Virtual environment activated (Windows)."
else
    echo "Error: Could not find activate script in virtual environment."
    exit 1
fi

# --- Step 2: Execute the test suite ---
echo "Running pytest test suite..."
pytest

# --- Step 3: Return exit code based on test results ---
# $? holds the exit status of the last executed command.
# pytest returns 0 for success, non-zero for failure.
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Tests failed. Please check the output above for details."
    exit 1
fi