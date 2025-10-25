"""Core image conversion functionality."""

from PIL import Image
from pathlib import Path
from typing import Tuple
from ..utils.metadata import extract_metadata, apply_metadata

# Register JPEG-XL plugin (auto-registers on import)
try:
    import pillow_jxl  # noqa: F401
except ImportError:
    pass  # Plugin not available

# Register HEIF/AVIF plugin
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass  # Plugin not available


class ImageConverter:
    """
    Image conversion engine supporting multiple modern formats.

    Supports: WebP, JPEG, JPEG-XL, AVIF, and optimized PNG.
    """

    SUPPORTED_FORMATS = {
        'webp': 'WEBP',
        'jpeg': 'JPEG',
        'jpeg-xl': 'JXL',  # Requires pillow-jxl-plugin
        'avif': 'AVIF',    # Requires pillow-heif
        'png': 'PNG'
    }

    def convert_single(
        self,
        input_path: Path,
        output_path: Path,
        output_format: str,
        quality: int = 85,
        lossless: bool = False,
    ) -> Tuple[bool, str]:
        """Convert a single image file.

        Args:
            input_path: Path to the input image
            output_path: Path to save the converted image
            output_format: Output format (webp, jpeg, jpeg-xl, avif, png)
            quality: Quality setting (0-100)
            lossless: Use lossless compression

        Returns:
            Tuple of (success, message)
        """
        try:
            # 1. Validate format
            pil_format = self.SUPPORTED_FORMATS.get(output_format.lower())
            if not pil_format:
                return False, f"Unsupported format: {output_format}"

            # 2. Load image
            with Image.open(input_path) as img:
                # 3. Extract metadata before conversion
                metadata = extract_metadata(img)

                # 4. Handle transparency for JPEG (no alpha support)
                if output_format.lower() == 'jpeg' and img.mode in ('RGBA', 'LA', 'P'):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = bg

                # 5. Prepare format-specific save options
                save_kwargs = self._get_save_kwargs(output_format.lower(), quality, lossless)

                # 6. Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # 7. Save image with format-specific options
                img.save(output_path, format=pil_format, **save_kwargs)

            # 8. Apply metadata to saved image
            apply_metadata(output_path, metadata)

            return True, f"Successfully converted to {output_format}"

        except Exception as e:
            return False, f"Conversion error: {str(e)}"

    def _get_save_kwargs(self, output_format: str, quality: int, lossless: bool) -> dict:
        """Get format-specific save parameters.

        Returns:
            Dictionary of kwargs for Image.save()
        """
        save_kwargs = {}

        if output_format == 'webp':
            save_kwargs['quality'] = quality
            save_kwargs['method'] = 6  # Best compression
            if lossless:
                save_kwargs['lossless'] = True
        elif output_format == 'jpeg':
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
        elif output_format == 'jpeg-xl':
            save_kwargs['quality'] = quality
            if lossless:
                save_kwargs['lossless'] = True
        elif output_format == 'avif':
            save_kwargs['quality'] = quality
        elif output_format == 'png':
            save_kwargs['optimize'] = True

        return save_kwargs
