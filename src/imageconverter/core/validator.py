"""Image file validation utilities."""

from pathlib import Path
from typing import Tuple
from PIL import Image


def is_valid_image(filepath: Path) -> Tuple[bool, str]:
    """Validate if a file is a valid PNG image.

    Args:
        filepath: Path to the image file

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.
    """
    # Basic checks
    if not filepath.exists():
        return False, "File does not exist"

    if not filepath.is_file():
        return False, "Path is not a file"

    if not filepath.suffix.lower() == ".png":
        return False, "File is not a PNG"

    # Check PNG magic bytes
    try:
        with open(filepath, 'rb') as f:
            header = f.read(8)
            # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
            if header != b'\x89PNG\r\n\x1a\n':
                return False, "File is not a valid PNG (wrong magic bytes)"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

    # Check if image can be opened and is not corrupted
    try:
        with Image.open(filepath) as img:
            img.verify()
        return True, ""
    except Exception as e:
        return False, f"Corrupted or invalid image: {str(e)}"
