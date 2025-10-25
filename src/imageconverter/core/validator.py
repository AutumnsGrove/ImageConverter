"""Image file validation utilities."""

from pathlib import Path
from typing import Tuple
from PIL import Image


# Supported image extensions
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.jxl', '.bmp', '.tiff', '.tif', '.gif'}


def is_valid_image(filepath: Path) -> Tuple[bool, str]:
    """Validate if a file is a valid image (any format supported by PIL).

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

    # Check if extension is supported
    if filepath.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file extension: {filepath.suffix}"

    # Try to open and verify image with PIL
    try:
        with Image.open(filepath) as img:
            img.verify()
        return True, ""
    except Exception as e:
        return False, f"Corrupted or invalid image: {str(e)}"
