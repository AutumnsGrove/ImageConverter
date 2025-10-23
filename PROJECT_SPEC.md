# ImageConverter - Project Specification

## Overview

ImageConverter is a cross-platform (macOS/Windows) batch image conversion tool with both CLI and GUI interfaces, optimized for converting PNG images to modern formats like WebP, JPEG-XL, and others. Built with Python and UV for fast, efficient image processing.

## Core Features

### Image Processing

- **Batch conversion** of PNG images to multiple formats:
  - WebP (primary)
  - JPEG
  - JPEG-XL
  - AVIF
  - PNG (optimized)
- **Metadata preservation** (EXIF data)
- **Quality matching** - maintain visual quality while reducing file size
- **Recursive processing** - handle nested folder structures
- **Multiprocessing** - configurable worker threads for performance

### CLI Interface

**Command names:** `ImageConverter` (primary), `imgconvert` (alias)

**Features:**

- Quality/compression control (0-100 scale)
- Lossless vs lossy toggle
- Recursive subfolder processing
- Custom output destination (default: ~/Downloads/ImageConverter_Output)
- Filename pattern options (preserve, add suffix)
- Progress bars with tqdm/rich
- Verbose logging mode
- Dry-run preview mode
- Worker thread configuration
- File validation

### GUI Interface

**Framework:** Tkinter (cross-platform, minimal dependencies)

**Features:**

- Folder selection dialog
- Drag-and-drop support
- Before/after preview panel
- Quality/format settings
- Progress indicator with batch status
- Worker thread configuration
- Conversion history/log viewer
- Failed files report
- Responsive design for different screen sizes

## Technical Stack

### Core

- **Language:** Python 3.10+
- **Package Manager:** UV
- **Image Processing:** Pillow (PIL)
- **CLI Framework:** Click or Typer
- **Progress Bars:** Rich (primary) or tqdm (fallback)
- **GUI:** Tkinter (built-in)
- **Multiprocessing:** Python concurrent.futures

### Optional Dependencies

- **pillow-heif** for HEIF/AVIF support
- **pillow-jpegxl** for JPEG-XL support (if needed)

## Architecture

```
imageconverter/
├── __init__.py
├── cli.py              # CLI entry point
├── gui.py              # GUI entry point
├── core/
│   ├── __init__.py
│   ├── converter.py    # Core conversion logic
│   ├── processor.py    # Batch processing with multiprocessing
│   ├── validator.py    # File validation
│   └── config.py       # Configuration management
├── utils/
│   ├── __init__.py
│   ├── metadata.py     # EXIF preservation
│   ├── logger.py       # Logging utilities
│   └── paths.py        # Path handling
└── tests/
    ├── __init__.py
    ├── test_converter.py
    ├── test_processor.py
    └── test_validator.py
```

## Installation

### Global Installation

```bash
uv tool install imageconverter
```

### Development Installation

```bash
git clone https://github.com/yourusername/imageconverter.git
cd imageconverter
uv sync
```

## Usage

### CLI

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

# Dry run
imgconvert /path/to/images --format webp --dry-run

# Multiple formats
imgconvert /path/to/images --format webp,jpeg-xl --quality 90
```

### GUI

```bash
# Launch GUI
imageconverter
# or
imgconvert --gui
```

## Configuration

### Default Settings

- **Output Location:** `~/Downloads/ImageConverter_Output/`
- **Format:** WebP
- **Quality:** 85 (lossy), 100 (lossless)
- **Workers:** CPU count - 1
- **Recursive:** True
- **Preserve Metadata:** True

### Config File

Location: `~/.config/imageconverter/config.yaml` (macOS/Linux) or `%APPDATA%/imageconverter/config.yaml` (Windows)

```yaml
defaults:
  format: webp
  quality: 85
  lossless: false
  output_dir: ~/Downloads/ImageConverter_Output
  workers: 4
  preserve_metadata: true
  recursive: true
  filename_pattern: "{name}_converted.{ext}"
```

## Error Handling

### Strategy

- **Continue on failure** - don’t stop batch processing
- **Collect errors** - aggregate failed files with error descriptions
- **Report at end** - display/log all failures with actionable messages
- **Graceful degradation** - skip problematic files, process remaining

### Common Errors

- Invalid/corrupted PNG files
- Insufficient disk space
- Permission errors
- Unsupported metadata formats
- Memory limitations

## Performance Targets

- **Small batches** (< 50 images): < 10 seconds
- **Medium batches** (50-500 images): 1-3 minutes
- **Large batches** (500+ images): Scales linearly with multiprocessing
- **Memory usage:** < 100MB base + ~10MB per worker thread
- **CPU utilization:** Configurable (default: n-1 cores)

## Cross-Platform Considerations

### macOS

- Native file dialogs
- Spotlight integration considerations
- Retina display support for previews

### Windows

- Windows file dialogs
- Windows path handling (backslashes)
- Windows Defender exclusions for performance

## Future Enhancements (Post-MVP)

- Batch rename functionality
- Image resizing options
- Watermarking
- Cloud storage integration
- Watch folder mode
- Plugin system for custom formats
- Web interface option