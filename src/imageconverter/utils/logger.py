"""Logging utilities for ImageConverter."""

import logging
from pathlib import Path
from typing import List, Dict, Any


class ErrorCollector:
    """Collects and categorizes errors during batch processing."""

    def __init__(self) -> None:
        """Initialize the error collector."""
        self.errors: List[Dict[str, Any]] = []

    def add_error(self, filepath: Path, error_type: str, message: str) -> None:
        """Add an error to the collection.

        Args:
            filepath: Path to the file that caused the error
            error_type: Type of error (e.g., 'validation', 'conversion', 'io')
            message: Error message
        """
        self.errors.append(
            {"filepath": str(filepath), "type": error_type, "message": message}
        )

    def get_errors(self) -> List[Dict[str, Any]]:
        """Get all collected errors.

        Returns:
            List of error dictionaries
        """
        return self.errors

    def get_errors_by_type(self, error_type: str) -> List[Dict[str, Any]]:
        """Get errors filtered by type.

        Args:
            error_type: Type of error to filter by

        Returns:
            List of filtered error dictionaries
        """
        return [e for e in self.errors if e["type"] == error_type]

    def clear(self) -> None:
        """Clear all collected errors."""
        self.errors.clear()


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration.

    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
