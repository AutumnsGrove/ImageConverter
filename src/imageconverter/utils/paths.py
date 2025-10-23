"""Path handling utilities."""

from pathlib import Path
import platform


def get_config_dir() -> Path:
    """Get the platform-specific configuration directory.

    Returns:
        Path to configuration directory
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        config_dir = Path.home() / ".config" / "imageconverter"
    elif system == "Windows":
        appdata = Path(platform.os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        config_dir = appdata / "imageconverter"
    else:  # Linux and others
        config_dir = Path.home() / ".config" / "imageconverter"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_default_output_dir() -> Path:
    """Get the default output directory.

    Returns:
        Path to default output directory
    """
    return Path.home() / "Downloads" / "ImageConverter_Output"


def ensure_dir_exists(path: Path) -> None:
    """Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists
    """
    path.mkdir(parents=True, exist_ok=True)
