"""Metadata extraction and preservation utilities."""

from pathlib import Path
from typing import Dict, Any
from PIL import Image


def extract_metadata(image: Image.Image) -> Dict[str, Any]:
    """Extract metadata from an image.

    Args:
        image: PIL Image object

    Returns:
        Dictionary containing EXIF and other metadata
    """
    metadata = {}

    # Extract EXIF data
    if hasattr(image, '_getexif') and image._getexif():
        metadata['exif'] = image.info.get('exif', b'')
    elif 'exif' in image.info:
        metadata['exif'] = image.info['exif']

    # Extract other metadata
    for key in ['dpi', 'transparency', 'gamma', 'icc_profile']:
        if key in image.info:
            metadata[key] = image.info[key]

    return metadata


def apply_metadata(output_path: Path, metadata: Dict[str, Any]) -> None:
    """Apply metadata to a saved image.

    Args:
        output_path: Path to the saved image
        metadata: Metadata dictionary from extract_metadata()
    """
    if not metadata:
        return

    try:
        with Image.open(output_path) as img:
            # Apply EXIF if present
            if 'exif' in metadata and metadata['exif']:
                # Need to save with exif parameter
                img.save(output_path, exif=metadata['exif'])
    except Exception:
        # Silently fail if metadata cannot be applied
        # (some formats don't support EXIF)
        pass
