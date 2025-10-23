# ImageConverter

A cross-platform (macOS/Windows) batch image conversion tool with both CLI and GUI interfaces, optimized for converting PNG images to modern formats like WebP, JPEG-XL, and others.

## Features

- **Batch Conversion**: Convert multiple PNG images at once
- **Multiple Formats**: WebP, JPEG, JPEG-XL, AVIF, and optimized PNG
- **Dual Interface**: Both CLI and GUI available
- **Metadata Preservation**: Maintains EXIF data during conversion
- **Quality Control**: Configurable quality settings and lossless options
- **Multiprocessing**: Fast batch processing with configurable worker threads
- **Progress Tracking**: Real-time progress bars and status updates

## Installation

### Using UV (Recommended)

```bash
# Install globally as a tool
uv tool install imageconverter

# Or install from source
git clone https://github.com/yourusername/imageconverter.git
cd imageconverter
uv sync
```

### Development Installation

```bash
git clone https://github.com/yourusername/imageconverter.git
cd imageconverter
uv sync
```

## Usage

### CLI Interface

```bash
# Basic conversion
imgconvert /path/to/images --format webp

# Advanced options
imgconvert /path/to/images \
  --format webp \
  --quality 85 \
  --recursive \
  --output ~/custom/output \
  --workers 4 \
  --verbose

# Dry run (preview without converting)
imgconvert /path/to/images --format webp --dry-run

# Multiple formats
imgconvert /path/to/images --format webp,jpeg-xl --quality 90
```

### GUI Interface

```bash
# Launch GUI
imageconverter

# Or from CLI
imgconvert --gui
```

## Supported Formats

- **WebP**: Modern format with excellent compression (lossy and lossless)
- **JPEG**: Universal compatibility (lossy only)
- **JPEG-XL**: Next-gen format with superior compression
- **AVIF**: High-efficiency image format
- **PNG**: Optimized PNG output

## Configuration

Default settings:
- **Output Location**: `~/Downloads/ImageConverter_Output/`
- **Format**: WebP
- **Quality**: 85 (lossy), 100 (lossless)
- **Workers**: CPU count - 1
- **Recursive**: True
- **Preserve Metadata**: True

Configuration file location:
- macOS/Linux: `~/.config/imageconverter/config.yaml`
- Windows: `%APPDATA%/imageconverter/config.yaml`

## Requirements

- Python 3.10 or higher
- UV package manager

## Development

### Project Structure

```
imageconverter/
├── src/
│   └── imageconverter/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point
│       ├── gui.py              # GUI entry point
│       ├── core/
│       │   ├── __init__.py
│       │   ├── converter.py    # Core conversion logic
│       │   ├── processor.py    # Batch processing
│       │   ├── validator.py    # File validation
│       │   └── config.py       # Configuration management
│       └── utils/
│           ├── __init__.py
│           ├── metadata.py     # EXIF preservation
│           ├── logger.py       # Logging utilities
│           └── paths.py        # Path handling
└── tests/
    └── __init__.py
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Format code
uv run black src/

# Lint code
uv run ruff check src/

# Type checking
uv run mypy src/
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run code quality checks
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [UV](https://github.com/astral-sh/uv) for fast package management
- Uses [Pillow](https://python-pillow.org/) for image processing
- CLI powered by [Click](https://click.palletsprojects.com/)
- Rich terminal output by [Rich](https://rich.readthedocs.io/)

## Status

⚠️ **Work in Progress**: This project is currently in early development. Core conversion functionality is being implemented.

## Roadmap

- [x] Project setup and structure
- [ ] Core image conversion engine
- [ ] CLI implementation
- [ ] GUI implementation
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] PyPI distribution
