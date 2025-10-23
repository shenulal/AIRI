#!/usr/bin/env python
"""Setup script to download required NLP models."""

import subprocess
import sys


def download_spacy_model():
    """Download spaCy English model."""
    print("Downloading spaCy English model...")
    try:
        subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
            check=True
        )
        print("✓ spaCy model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to download spaCy model: {e}")
        return False
    return True


def main():
    """Download all required models."""
    print("Setting up NLP models...")
    print()
    
    success = True
    
    # Download spaCy model
    if not download_spacy_model():
        success = False
    
    print()
    if success:
        print("✓ All models downloaded successfully!")
        return 0
    else:
        print("✗ Some models failed to download")
        return 1


if __name__ == "__main__":
    sys.exit(main())

