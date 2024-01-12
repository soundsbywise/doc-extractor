#!/bin/bash
set -e

# Check if python3 is available
if command -v python3 &> /dev/null; then
    echo "Creating a virtual enviornment."
    python3 -m venv venv
    echo "Activating virtual enviornment."
    source venv/bin/activate
    echo "Installing python requirements."
    python3 -m pip install -r server/requirements.txt
else
    echo "Python 3 is not installed or not on the PATH. Please install Python 3 and make sure it is accessible via the python3 command."
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Please install Homebrew first."
    exit 1
fi

# Check if poppler is installed
if brew list --formula | grep -q "poppler"; then
    echo "poppler is installed."
else
    echo "poppler is not installed. Installing poppler..."
    brew install poppler
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "OPENAI_API_KEY is not set. Please set the environment variable before and re-run the script."
    exit 1
else
    echo "All done!"
fi