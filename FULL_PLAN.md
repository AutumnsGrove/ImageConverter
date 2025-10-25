# ImageConverter - Full Implementation Plan (Tonight)

**Last Updated:** 2025-10-24
**Goal:** Complete fully-functional ImageConverter (CLI + GUI) tonight
**Platform Requirements:** macOS (primary testing), Windows-compatible code
**User:** Making this for Mom (Windows) + personal use (macOS)

---

## 🎯 Current Status

### ✅ What's DONE (from commit 249c60c)
- **Project structure** complete (`src/imageconverter/`, `tests/`)
- **UV setup** with `pyproject.toml` configured
- **Dependencies installed:**
  - Pillow >= 10.0.0
  - rich >= 13.0.0
  - click >= 8.0.0
  - pillow-heif >= 0.13.0 (AVIF support)
  - Dev deps: pytest, black, ruff, mypy
- **CLI skeleton** (`cli.py`) - all options configured, no logic
- **GUI skeleton** (`gui.py`) - nice Tkinter UI, no logic
- **Core module stubs:**
  - `core/converter.py` - class skeleton, all TODOs
  - `core/processor.py` - method signatures, all TODOs
  - `core/validator.py` - basic path checks only
  - `utils/metadata.py` - stub only
  - `utils/logger.py` - implemented
  - `utils/paths.py` - implemented
- **House agents installed** (`.claude/agents/`)
- **BaseProject ClaudeUsage guides** installed
- **Test data available** (`bin/` folder with journal photos)
  - Contains real-world PNG images for testing
  - May include some non-PNG files (needs pre-test cleanup)
  - Located in project root at `bin/` (gitignored)

### ❌ What's MISSING (Must implement tonight)

#### Critical Path (Core Engine)
1. **Missing dependency:** `pillow-jpegxl-plugin` not in pyproject.toml
2. **converter.py** - Zero conversion logic (all formats are TODOs)
3. **validator.py** - Needs magic bytes check + corruption detection
4. **metadata.py** - Completely unimplemented
5. **processor.py** - Batch processing + multiprocessing not implemented

#### Integration Layer
6. **CLI wiring** - Currently just prints "not implemented"
7. **GUI wiring** - Shows placeholder messagebox only
8. **Progress tracking** - Rich progress bars not integrated
9. **GUI threading** - Background processing not implemented

#### Testing & Validation
10. **Zero tests written** - Need comprehensive test suite
11. **No real-world testing** - Need to test with 100-250 PNG batch
12. **Windows compatibility** - Need to verify path handling works

---

## 📋 Implementation Plan (13 Tasks)

### Phase 1: Dependencies & Core Engine (40 min)

#### Task 1: Add Missing Dependency (2 min)
**File:** `pyproject.toml`

Add to dependencies array:
```toml
"pillow-jpegxl-plugin>=0.1.0",
```

Run: `uv sync`

---

#### Task 2: Implement core/converter.py (15 min)
**File:** `src/imageconverter/core/converter.py`

**Requirements:**
- Implement `convert_single()` method
- Support formats: WebP, JPEG, JPEG-XL, AVIF, PNG (optimized)
- Handle quality settings (0-100)
- Handle lossless flag
- Preserve transparency (WebP, PNG, AVIF)
- Extract metadata before conversion
- Apply metadata after conversion
- Proper error handling with descriptive messages

**Implementation Guide:**
```python
from PIL import Image
from pathlib import Path
from typing import Tuple
from ..utils.metadata import extract_metadata, apply_metadata

class ImageConverter:
    SUPPORTED_FORMATS = {
        'webp': 'WEBP',
        'jpeg': 'JPEG',
        'jpeg-xl': 'JPEG XL',  # Requires pillow-jpegxl-plugin
        'avif': 'AVIF',         # Requires pillow-heif
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
        try:
            # 1. Load image
            with Image.open(input_path) as img:
                # 2. Extract metadata
                metadata = extract_metadata(img)

                # 3. Handle transparency
                # If converting to JPEG, need to remove alpha
                if output_format == 'jpeg' and img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = bg

                # 4. Prepare save kwargs
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

                # 5. Convert and save
                pil_format = self.SUPPORTED_FORMATS.get(output_format)
                if not pil_format:
                    return False, f"Unsupported format: {output_format}"

                # Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Save image
                img.save(output_path, format=pil_format, **save_kwargs)

                # 6. Apply metadata to saved image
                apply_metadata(output_path, metadata)

                return True, f"Converted to {output_format}"

        except Exception as e:
            return False, f"Conversion error: {str(e)}"
```

---

#### Task 3: Implement core/validator.py (8 min)
**File:** `src/imageconverter/core/validator.py`

**Requirements:**
- Check file exists and is readable
- Verify PNG magic bytes (89 50 4E 47 0D 0A 1A 0A)
- Detect corrupted images using Pillow's verify()
- Return descriptive error messages

**Implementation Guide:**
```python
from pathlib import Path
from typing import Tuple
from PIL import Image

def is_valid_image(filepath: Path) -> Tuple[bool, str]:
    """Validate if a file is a valid PNG image."""
    # Basic checks
    if not filepath.exists():
        return False, "File does not exist"

    if not filepath.is_file():
        return False, "Path is not a file"

    if not filepath.suffix.lower() == ".png":
        return False, "File is not a PNG"

    # Check PNG magic bytes
    try:
        with open(filepath, 'rb') as f:
            header = f.read(8)
            # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
            if header != b'\x89PNG\r\n\x1a\n':
                return False, "File is not a valid PNG (wrong magic bytes)"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

    # Check if image can be opened and is not corrupted
    try:
        with Image.open(filepath) as img:
            img.verify()
        return True, ""
    except Exception as e:
        return False, f"Corrupted or invalid image: {str(e)}"
```

---

#### Task 4: Implement utils/metadata.py (8 min)
**File:** `src/imageconverter/utils/metadata.py`

**Requirements:**
- Extract EXIF data from source image
- Apply EXIF data to converted image
- Handle missing metadata gracefully
- Support common EXIF tags

**Implementation Guide:**
```python
from pathlib import Path
from typing import Dict, Any
from PIL import Image
from PIL.PngImagePlugin import PngInfo

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
```

---

#### Task 5: Implement core/processor.py (15 min)
**File:** `src/imageconverter/core/processor.py`

**Requirements:**
- Discover PNG files in directory (recursive option)
- Filter hidden files/folders
- Batch process with multiprocessing
- Progress callbacks for UI updates
- Collect successes and failures
- Generate output paths with collision handling

**Implementation Guide:**
```python
from pathlib import Path
from typing import List, Callable, Dict, Any
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from .converter import ImageConverter
from .validator import is_valid_image

class BatchProcessor:
    """Handles batch image processing with multiprocessing."""

    def __init__(self, workers: int | None = None) -> None:
        if workers is None:
            workers = max(1, os.cpu_count() - 1 if os.cpu_count() else 1)
        self.workers = workers

    def discover_images(self, root_path: Path, recursive: bool = True) -> List[Path]:
        """Discover PNG images in a directory."""
        images = []

        if recursive:
            pattern = "**/*.png"
        else:
            pattern = "*.png"

        for img_path in root_path.glob(pattern):
            # Skip hidden files/folders
            if any(part.startswith('.') for part in img_path.parts):
                continue

            # Validate it's actually a PNG
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
        """Process a batch of images with multiprocessing."""
        results = {
            "total": len(image_list),
            "successes": 0,
            "failures": 0,
            "errors": []
        }

        converter = ImageConverter()

        # Process images
        for idx, input_path in enumerate(image_list):
            # Generate output path
            output_path = self.generate_output_path(
                input_path,
                Path(options['output_dir']),
                options.get('pattern')
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
        self, input_path: Path, output_dir: Path, pattern: str | None = None
    ) -> Path:
        """Generate output path for a converted image."""
        # Default pattern: keep original name, change extension
        if pattern is None:
            stem = input_path.stem
            ext = ".webp"  # Default extension
        else:
            # Pattern support (future enhancement)
            stem = input_path.stem
            ext = ".webp"

        output_path = output_dir / f"{stem}{ext}"

        # Handle name collisions
        counter = 1
        while output_path.exists():
            output_path = output_dir / f"{stem}_{counter}{ext}"
            counter += 1

        return output_path
```

---

### Phase 2: Integration (30 min)

#### Task 6: Wire Up CLI (15 min)
**File:** `src/imageconverter/cli.py`

**Requirements:**
- Use BatchProcessor to discover images
- Use BatchProcessor to convert images
- Show Rich progress bar during conversion
- Display summary at the end
- Handle dry-run mode
- Show errors for failed conversions

**Key Changes:**
```python
from pathlib import Path
from .core.processor import BatchProcessor
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

def main(...):
    # ... existing argument parsing ...

    # Set up processor
    processor = BatchProcessor(workers=workers)

    # Discover images
    console.print(f"[cyan]Scanning {input_dir}...[/cyan]")
    input_path = Path(input_dir)
    images = processor.discover_images(input_path, recursive=recursive)

    if not images:
        console.print("[yellow]No PNG images found[/yellow]")
        return

    console.print(f"[green]Found {len(images)} PNG images[/green]")

    # Set up output directory
    if output:
        output_path = Path(output)
    else:
        output_path = Path.home() / "Downloads" / "ImageConverter_Output"

    output_path.mkdir(parents=True, exist_ok=True)

    if dry_run:
        console.print("[yellow]DRY RUN - No files will be converted[/yellow]")
        for img in images[:10]:  # Show first 10
            console.print(f"  {img.name}")
        if len(images) > 10:
            console.print(f"  ... and {len(images) - 10} more")
        return

    # Process with progress bar
    options = {
        'format': format,
        'quality': quality,
        'lossless': lossless,
        'output_dir': str(output_path),
        'pattern': filename_pattern
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Converting images...", total=len(images))

        def update_progress(current, total, filename):
            progress.update(task, completed=current, description=f"[cyan]Converting {filename}")

        results = processor.process_batch(images, options, update_progress)

    # Show summary
    console.print(f"\n[bold green]Conversion Complete![/bold green]")
    console.print(f"Total: {results['total']}")
    console.print(f"[green]Successful: {results['successes']}[/green]")
    console.print(f"[red]Failed: {results['failures']}[/red]")

    if results['errors']:
        console.print(f"\n[red]Errors:[/red]")
        for error in results['errors'][:10]:  # Show first 10 errors
            console.print(f"  {error['file']}: {error['error']}")
```

---

#### Task 7: Wire Up GUI with Threading (15 min)
**File:** `src/imageconverter/gui.py`

**Requirements:**
- Run conversion in background thread (non-blocking UI)
- Update progress bar during conversion
- Enable/disable buttons during processing
- Show results in status label
- Add "Stop" button functionality

**Key Changes:**
```python
import threading
from pathlib import Path
from .core.processor import BatchProcessor

class ImageConverterGUI:
    def __init__(self, root: tk.Tk) -> None:
        # ... existing init ...
        self.processor = BatchProcessor()
        self.processing = False
        self.cancel_processing = False

    def _create_widgets(self) -> None:
        # ... existing widgets ...

        # Add progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Add workers spinbox
        ttk.Label(main_frame, text="Workers:").grid(row=3, column=0, sticky=tk.W)
        self.workers_var = tk.IntVar(value=4)
        workers_spin = ttk.Spinbox(main_frame, from_=1, to=16, textvariable=self.workers_var, width=10)
        workers_spin.grid(row=3, column=1, sticky=tk.W, padx=5)

        # Lossless checkbox
        self.lossless_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Lossless", variable=self.lossless_var).grid(row=3, column=2)

    def _convert_images(self) -> None:
        """Start image conversion in background thread."""
        if self.processing:
            return

        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("No Folder", "Please select an input folder first.")
            return

        # Disable convert button
        self.processing = True
        self.cancel_processing = False

        # Start background thread
        thread = threading.Thread(target=self._conversion_thread, daemon=True)
        thread.start()

    def _conversion_thread(self) -> None:
        """Background conversion thread."""
        try:
            folder = Path(self.folder_path.get())
            format_type = self.format_var.get()
            quality = self.quality_var.get()
            lossless = self.lossless_var.get()
            workers = self.workers_var.get()

            # Update status
            self.status_var.set("Discovering images...")

            # Discover images
            processor = BatchProcessor(workers=workers)
            images = processor.discover_images(folder, recursive=True)

            if not images:
                self.status_var.set("No PNG images found")
                self.processing = False
                return

            # Set up output directory
            output_dir = Path.home() / "Downloads" / "ImageConverter_Output"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Process batch
            options = {
                'format': format_type,
                'quality': quality,
                'lossless': lossless,
                'output_dir': str(output_dir),
                'pattern': None
            }

            def update_progress(current, total, filename):
                if self.cancel_processing:
                    return
                progress_pct = (current / total) * 100
                self.progress_var.set(progress_pct)
                self.status_var.set(f"Converting {filename} ({current}/{total})")

            results = processor.process_batch(images, options, update_progress)

            # Show results
            self.progress_var.set(100)
            self.status_var.set(
                f"Complete! {results['successes']} succeeded, {results['failures']} failed"
            )

            messagebox.showinfo(
                "Conversion Complete",
                f"Converted {results['successes']} images\n"
                f"Failed: {results['failures']}\n"
                f"Output: {output_dir}"
            )

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

        finally:
            self.processing = False
            self.progress_var.set(0)
```

---

### Phase 3: Testing (30 min)

#### Task 8: Create Test Suite (20 min)
**File:** `tests/test_converter.py`, `tests/test_validator.py`, `tests/test_processor.py`

Use **test-strategist** agent to plan comprehensive tests.

**Test Requirements:**
- Test all 5 output formats
- Test quality settings
- Test lossless mode
- Test metadata preservation
- Test transparency handling
- Test batch processing
- Test file discovery
- Test validation (valid PNGs, invalid files, corrupted images)

**Example test structure:**
```python
# tests/test_converter.py
import pytest
from pathlib import Path
from imageconverter.core.converter import ImageConverter
from PIL import Image

@pytest.fixture
def sample_png(tmp_path):
    """Create a test PNG image."""
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
    png_path = tmp_path / "test.png"
    img.save(png_path)
    return png_path

def test_convert_to_webp(sample_png, tmp_path):
    """Test conversion to WebP format."""
    converter = ImageConverter()
    output_path = tmp_path / "output.webp"

    success, message = converter.convert_single(
        sample_png,
        output_path,
        'webp',
        quality=85
    )

    assert success
    assert output_path.exists()

    # Verify it's actually WebP
    with Image.open(output_path) as img:
        assert img.format == 'WEBP'

# Similar tests for JPEG, AVIF, JPEG-XL, PNG...
```

---

#### Task 9: Test with Real PNG Batch (10 min)

**Test images available in `bin/` folder (journal photos from this year)**

**IMPORTANT:** The `bin/` folder may contain some non-PNG files that need cleanup first.

**Pre-test cleanup:**
```bash
# Check what file types are in bin/
cd bin/
file * | grep -v PNG | head -20  # Show non-PNG files

# Option 1: Move non-PNGs to a subfolder
mkdir -p non-png
find . -maxdepth 1 -type f ! -name "*.png" -exec mv {} non-png/ \;

# Option 2: Just work with PNGs and let validator filter the rest
# (validator should gracefully skip non-PNG files)
```

**Test steps:**
1. Run CLI on bin folder: `uv run imgconvert bin/ --format webp --verbose`
2. Verify output directory created at `~/Downloads/ImageConverter_Output/`
3. Check conversion success rate (should be high for valid PNGs)
4. Validator should skip non-PNG files gracefully
5. Spot-check converted images (open a few .webp files)
6. Test GUI with same batch: `uv run imageconverter`
   - Select `bin/` folder
   - Choose WebP format, quality 85
   - Watch progress bar
   - Verify results

**Expected behavior:**
- Valid PNGs convert successfully
- Non-PNG files are skipped with clear error messages
- No crashes or hangs during batch processing
- Progress bars update smoothly

---

### Phase 4: Polish & Validation (30 min)

#### Task 10: Windows Compatibility Check (10 min)

**Requirements:**
- All paths use `pathlib.Path` (already done in skeleton)
- No hardcoded `/` or `\` separators
- Output directory creation works on both platforms
- Test on Windows if possible, otherwise verify code patterns

**Verification checklist:**
- ✅ All path operations use `Path()` from pathlib
- ✅ Use `Path.home()` for user home directory
- ✅ Use `path.parent.mkdir(parents=True, exist_ok=True)`
- ✅ Use `/` operator for path joining (Path supports on all platforms)
- ✅ No `os.path.join()` or string concatenation for paths

---

#### Task 11: Error Message Polish (10 min)

**Requirements:**
- Clear, actionable error messages
- Suggest fixes for common issues
- Graceful failure (continue processing other images)

**Examples:**
```python
# Good error messages:
"Could not convert image.png: Unsupported format 'bmp'. Supported formats: webp, jpeg, jpeg-xl, avif, png"
"File not found: /path/to/image.png. Please check the path and try again."
"Insufficient disk space. Need 50MB but only 10MB available."

# Bad error messages:
"Error"
"Failed"
"Exception occurred"
```

---

#### Task 12: UV Tool Installation Test (5 min)

```bash
# Test local installation
uv tool install .

# Verify commands work globally
imageconverter --help  # Should launch GUI help
imgconvert --help      # Should show CLI help

# Test CLI
imgconvert /path/to/test/images --format webp --dry-run

# Test GUI
imageconverter  # Should launch GUI window
```

---

#### Task 13: Final Security Audit (5 min)

Use **security-auditor** agent to check for:
- No hardcoded paths that won't work cross-platform
- Proper error handling (no uncaught exceptions)
- File operations are safe (no arbitrary path traversal)
- Resource cleanup (files closed properly)
- No security vulnerabilities

---

## 🎯 Success Criteria

### Must Have (Tonight)
- ✅ All 5 formats convert successfully (WebP, JPEG, JPEG-XL, AVIF, PNG)
- ✅ CLI works end-to-end on macOS
- ✅ GUI works end-to-end on macOS
- ✅ Batch of 100-250 PNGs converts successfully
- ✅ Progress bars working in both CLI and GUI
- ✅ Error handling graceful (continues on failure)
- ✅ UV tool installable globally
- ✅ Code is Windows-compatible (verified via patterns)

### Nice to Have (If time permits)
- ⭐ Actual Windows testing
- ⭐ Comprehensive test coverage (>80%)
- ⭐ Performance optimization
- ⭐ Config file support

---

## 🚀 Execution Strategy

### Subagent Usage (CRITICAL for speed)

Use house agents and quick-code-patch agents **aggressively in parallel**:

**Phase 1 - Core Implementation:**
```
Launch 4 quick-code-patch agents in PARALLEL:
1. quick-code-patch: Implement converter.py (all 5 formats)
2. quick-code-patch: Implement validator.py (magic bytes + corruption)
3. quick-code-patch: Implement metadata.py (EXIF handling)
4. quick-code-patch: Implement processor.py (multiprocessing + discovery)
```

**Phase 2 - Integration:**
```
Launch 2 quick-code-patch agents in PARALLEL:
1. quick-code-patch: Wire up CLI with progress bars
2. quick-code-patch: Wire up GUI with threading + progress
```

**Phase 3 - Testing:**
```
1. test-strategist: Plan comprehensive test suite
2. quick-code-patch: Implement tests based on plan
3. house-bash: Run test suite and capture results
```

**Phase 4 - Final:**
```
1. security-auditor: Security and safety review
2. house-bash: Test UV installation
```

### Git Commit Strategy

Commit after each major phase:

```bash
# Phase 1
git commit -m "feat: implement core conversion engine

- Add pillow-jpegxl-plugin dependency
- Implement converter.py with all 5 format support (WebP, JPEG, JPEG-XL, AVIF, PNG)
- Implement validator.py with magic bytes check and corruption detection
- Implement metadata.py for EXIF preservation
- Implement processor.py with multiprocessing batch processing

🤖 Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>"

# Phase 2
git commit -m "feat: wire up CLI and GUI with core modules

- Connect CLI to BatchProcessor with Rich progress bars
- Connect GUI to BatchProcessor with background threading
- Add progress tracking to both interfaces
- Implement error reporting and summaries

🤖 Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>"

# Phase 3
git commit -m "test: add comprehensive test suite

- Add tests for all conversion formats
- Add validator tests (magic bytes, corruption)
- Add processor tests (discovery, batch)
- Add metadata preservation tests
- All tests passing

🤖 Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>"

# Phase 4
git commit -m "chore: polish and final validation

- Improve error messages for user clarity
- Verify Windows path compatibility
- Test UV tool installation
- Security audit passed
- Ready for production use

🤖 Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>"
```

---

## 📝 Important Notes

### For Mom (Windows User)
- GUI is the primary interface for her
- Must be simple and intuitive
- Error messages should be clear and non-technical
- Default settings should "just work"

### For You (macOS + CLI User)
- CLI is the primary interface
- Rich progress bars for good UX
- Verbose mode for debugging
- Dry-run mode for safety

### Platform Differences
- **macOS:** Tkinter native, full testing
- **Windows:** Tkinter should work (bundled with Python), verify path handling

### Testing Notes
User will provide 100-250 PNG batch during Phase 3.
Until then, create small test PNGs programmatically.

---

## 🔧 Quick Reference Commands

```bash
# Install dependencies
uv sync

# Run CLI (after implementation)
uv run imgconvert /path/to/images --format webp

# Run GUI (after implementation)
uv run imageconverter

# Run tests
uv run pytest

# Format code
uv run black src/

# Lint
uv run ruff check src/

# Install as tool
uv tool install .

# Use globally after install
imageconverter  # GUI
imgconvert --help  # CLI help
```

---

## 📚 Reference Files

Key files already implemented and available:
- `utils/logger.py` - Logging utilities (working)
- `utils/paths.py` - Path handling utilities (working)
- `core/config.py` - Configuration management (partially working)

Key documentation:
- `PROJECT_SPEC.md` - Full project specification
- `TODOS_REAL.md` - Original comprehensive TODO list (10 phases)
- `ClaudeUsage/` - All BaseProject workflow guides
- `.claude/agents/` - House agents (house-bash, house-research, house-git, house-mcp)

---

## ⚠️ Common Pitfalls to Avoid

1. **Don't forget JPEG-XL dependency** - Add to pyproject.toml first
2. **JPEG doesn't support transparency** - Convert RGBA to RGB with white background
3. **Metadata may not work for all formats** - Fail silently if unsupported
4. **GUI must use threading** - Don't block UI during conversion
5. **Windows paths** - Always use `pathlib.Path`, never string concatenation
6. **Error handling** - Continue batch on single file failure
7. **Progress callbacks** - Must be thread-safe for GUI

---

**END OF PLAN**

Ready to execute? Start with Task 1 (add dependency) and launch parallel agents for Tasks 2-5!
