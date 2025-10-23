"""Image file validation utilities."""

from pathlib import Path
from typing import Tuple


def is_valid_image(filepath: Path) -> Tuple[bool, str]:
    """Validate if a file is a valid PNG image.

    Args:
        filepath: Path to the image file

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.
    """
    if not filepath.exists():
        return False, "File does not exist"

    if not filepath.is_file():
        return False, "Path is not a file"

    if not filepath.suffix.lower() == ".png":
        return False, "File is not a PNG"

    # TODO: Implement magic bytes check
    # TODO: Implement corruption detection

    return True, ""
