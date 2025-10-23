"""Configuration management for ImageConverter."""

from pathlib import Path
from typing import Any


class Config:
    """Configuration manager for ImageConverter."""

    DEFAULT_FORMAT = "webp"
    DEFAULT_QUALITY = 85
    DEFAULT_LOSSLESS = False
    DEFAULT_RECURSIVE = True
    DEFAULT_PRESERVE_METADATA = True

    def __init__(self) -> None:
        """Initialize configuration with defaults."""
        self.format = self.DEFAULT_FORMAT
        self.quality = self.DEFAULT_QUALITY
        self.lossless = self.DEFAULT_LOSSLESS
        self.recursive = self.DEFAULT_RECURSIVE
        self.preserve_metadata = self.DEFAULT_PRESERVE_METADATA
        self.output_dir = self._get_default_output_dir()

    @staticmethod
    def _get_default_output_dir() -> Path:
        """Get the default output directory."""
        return Path.home() / "Downloads" / "ImageConverter_Output"

    def load_from_file(self, config_path: Path) -> None:
        """Load configuration from a file.

        Args:
            config_path: Path to the configuration file
        """
        # TODO: Implement config file loading
        pass

    def save_to_file(self, config_path: Path) -> None:
        """Save configuration to a file.

        Args:
            config_path: Path to save the configuration file
        """
        # TODO: Implement config file saving
        pass
