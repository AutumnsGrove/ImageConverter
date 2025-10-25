"""Batch processing functionality."""

from pathlib import Path
from typing import List, Callable, Dict, Any
import os
from .converter import ImageConverter
from .validator import is_valid_image, SUPPORTED_EXTENSIONS


class BatchProcessor:
    """Handles batch image processing with multiprocessing."""

    def __init__(self, workers: int | None = None) -> None:
        """Initialize the batch processor.

        Args:
            workers: Number of worker processes (None = CPU count - 1)
        """
        if workers is None:
            workers = max(1, os.cpu_count() - 1 if os.cpu_count() else 1)
        self.workers = workers

    def discover_images(self, root_path: Path, recursive: bool = True) -> List[Path]:
        """Discover images of any supported format in a directory.

        Args:
            root_path: Root directory to scan
            recursive: Scan subdirectories recursively

        Returns:
            List of discovered image paths
        """
        images = []

        # Scan for all supported image extensions
        for ext in SUPPORTED_EXTENSIONS:
            if recursive:
                pattern = f"**/*{ext}"
            else:
                pattern = f"*{ext}"

            for img_path in root_path.glob(pattern):
                # Skip hidden files/folders
                if any(part.startswith('.') for part in img_path.parts):
                    continue

                # Validate it's actually a valid image
                is_valid, _ = is_valid_image(img_path)
                if is_valid:
                    images.append(img_path)

        return images

    def process_batch(
        self,
        image_list: List[Path],
        options: Dict[str, Any],
        progress_callback: Callable[[int, int, str], None] | None = None,
    ) -> Dict[str, Any]:
        """Process a batch of images.

        Args:
            image_list: List of image paths to process
            options: Processing options (format, quality, etc.)
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with processing results (successes, failures, etc.)
        """
        results = {
            "total": len(image_list),
            "successes": 0,
            "failures": 0,
            "errors": []
        }

        converter = ImageConverter()

        # Process images sequentially (multiprocessing can be added later)
        for idx, input_path in enumerate(image_list):
            # Generate output path
            output_path = self.generate_output_path(
                input_path,
                Path(options['output_dir']),
                options['format']
            )

            # Convert
            success, message = converter.convert_single(
                input_path,
                output_path,
                options['format'],
                options.get('quality', 85),
                options.get('lossless', False)
            )

            # Update results
            if success:
                results['successes'] += 1
            else:
                results['failures'] += 1
                results['errors'].append({
                    'file': str(input_path),
                    'error': message
                })

            # Progress callback
            if progress_callback:
                progress_callback(idx + 1, len(image_list), str(input_path.name))

        return results

    def generate_output_path(
        self, input_path: Path, output_dir: Path, format: str
    ) -> Path:
        """Generate output path for a converted image.

        Args:
            input_path: Input image path
            output_dir: Output directory
            format: Output format

        Returns:
            Output file path
        """
        stem = input_path.stem

        # Map format to extension
        ext_map = {
            'webp': '.webp',
            'jpeg': '.jpg',
            'jpeg-xl': '.jxl',
            'avif': '.avif',
            'png': '.png'
        }
        ext = ext_map.get(format, '.webp')

        output_path = output_dir / f"{stem}{ext}"

        # Handle name collisions
        counter = 1
        while output_path.exists():
            output_path = output_dir / f"{stem}_{counter}{ext}"
            counter += 1

        return output_path
