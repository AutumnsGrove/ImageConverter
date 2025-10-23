# ImageConverter - Implementation TODO

## Phase 1: Project Setup & Infrastructure

### 1.1 Project Initialization

- [ ] Initialize UV project with `uv init`
- [ ] Set up `pyproject.toml` with project metadata
  - [ ] Define project name, version, description
  - [ ] Set Python version requirement (>=3.10)
  - [ ] Configure entry points for CLI commands
    - [ ] `imageconverter` (main GUI launcher)
    - [ ] `imgconvert` (CLI tool)
- [ ] Create directory structure
  
  ```
  imageconverter/
  ├── __init__.py
  ├── cli.py
  ├── gui.py
  ├── core/
  ├── utils/
  └── tests/
  ```
- [ ] Initialize git repository with appropriate `.gitignore`
- [ ] Create `README.md` with installation and usage instructions

### 1.2 Dependencies

- [ ] Add core dependencies to `pyproject.toml`
  - [ ] Pillow (>=10.0.0)
  - [ ] rich (>=13.0.0) - for progress bars and CLI formatting
  - [ ] click (>=8.0.0) - for CLI framework
  - [ ] pillow-heif - for AVIF support
  - [ ] pillow-jpegxl-plugin - for JPEG-XL support
- [ ] Add development dependencies
  - [ ] pytest
  - [ ] pytest-cov
  - [ ] black (formatting)
  - [ ] ruff (linting)
  - [ ] mypy (type checking)
- [ ] Run `uv sync` to create lock file

### 1.3 Configuration System

- [ ] Create `core/config.py`
  - [ ] Define default configuration values
  - [ ] Implement config file loading (YAML)
  - [ ] Support for platform-specific config paths
    - [ ] macOS/Linux: `~/.config/imageconverter/`
    - [ ] Windows: `%APPDATA%/imageconverter/`
  - [ ] Environment variable overrides
  - [ ] Config validation and error handling
- [ ] Create default `config.yaml` template

-----

## Phase 2: Core Image Conversion Engine

### 2.1 Image Validation

- [ ] Create `core/validator.py`
  - [ ] Implement `is_valid_image(filepath)` function
  - [ ] Check file exists and is readable
  - [ ] Verify file is actually a PNG (magic bytes check)
  - [ ] Detect corrupted images
  - [ ] Return validation result with error details
- [ ] Add unit tests for validation edge cases

### 2.2 Metadata Preservation

- [ ] Create `utils/metadata.py`
  - [ ] Implement `extract_metadata(image)` using Pillow’s EXIF
  - [ ] Implement `apply_metadata(image, metadata)`
  - [ ] Handle missing/incomplete metadata gracefully
  - [ ] Support common EXIF tags
  - [ ] Test with images with and without metadata
- [ ] Test metadata preservation across formats

### 2.3 Core Converter

- [ ] Create `core/converter.py`
  - [ ] Implement `ImageConverter` class
  - [ ] Method: `convert_single(input_path, output_path, format, quality, lossless)`
    - [ ] Load image with Pillow
    - [ ] Extract metadata
    - [ ] Perform conversion with specified parameters
    - [ ] Apply metadata to output
    - [ ] Handle transparency (for WebP, PNG)
    - [ ] Return success/failure with details
  - [ ] Support formats:
    - [ ] WebP (lossy and lossless)
    - [ ] JPEG (lossy only)
    - [ ] JPEG-XL (lossy and lossless)
    - [ ] AVIF (lossy and lossless)
    - [ ] PNG (optimized)
  - [ ] Quality parameter handling (0-100 scale)
  - [ ] Error handling with descriptive messages
- [ ] Unit tests for each format
- [ ] Integration tests with sample images

### 2.4 Batch Processor

- [ ] Create `core/processor.py`
  - [ ] Implement `BatchProcessor` class
  - [ ] Method: `discover_images(root_path, recursive)`
    - [ ] Scan directory for PNG files
    - [ ] Support recursive subfolder scanning
    - [ ] Filter hidden files/folders
    - [ ] Return list of discovered image paths
  - [ ] Method: `process_batch(image_list, options, progress_callback)`
    - [ ] Set up multiprocessing pool (configurable workers)
    - [ ] Process images in parallel
    - [ ] Collect results (successes and failures)
    - [ ] Call progress_callback for UI updates
    - [ ] Handle worker exceptions gracefully
  - [ ] Method: `generate_output_path(input_path, output_dir, pattern)`
    - [ ] Support filename patterns
    - [ ] Preserve folder structure (optional)
    - [ ] Handle name collisions
  - [ ] Implement dry-run mode (simulation without writing)
- [ ] Test with various batch sizes
- [ ] Test multiprocessing with different worker counts

-----

## Phase 3: CLI Implementation

### 3.1 CLI Framework

- [ ] Create `cli.py`
  - [ ] Set up Click/Typer CLI application
  - [ ] Define main command group
  - [ ] Configure global options (verbose, config file)
  - [ ] Set up logging with configurable levels

### 3.2 Convert Command

- [ ] Implement `convert` command (main CLI function)
  - [ ] Positional argument: input directory
  - [ ] Option: `--format` (choices: webp, jpeg, jpeg-xl, avif, png)
  - [ ] Option: `--quality` (0-100, default 85)
  - [ ] Option: `--lossless` (flag)
  - [ ] Option: `--recursive` (flag, default True)
  - [ ] Option: `--output` (path, default ~/Downloads/ImageConverter_Output)
  - [ ] Option: `--workers` (int, default CPU count - 1)
  - [ ] Option: `--dry-run` (flag)
  - [ ] Option: `--verbose` (flag)
  - [ ] Option: `--filename-pattern` (string template)
- [ ] Input validation and error messages
- [ ] Connect to `BatchProcessor` backend

### 3.3 Progress Display

- [ ] Integrate Rich progress bars
  - [ ] Overall progress bar (total images)
  - [ ] Current file indicator
  - [ ] Processing speed (images/sec)
  - [ ] ETA calculation
  - [ ] Success/failure counters
- [ ] Verbose mode logging
  - [ ] Show each file being processed
  - [ ] Display conversion details (size reduction, format)
  - [ ] Log warnings and errors in real-time

### 3.4 Results Reporting

- [ ] Implement end-of-batch summary
  - [ ] Total images processed
  - [ ] Successful conversions
  - [ ] Failed conversions with file list
  - [ ] Total time elapsed
  - [ ] Average processing speed
  - [ ] Total space saved
- [ ] Error report formatting
  - [ ] Group errors by type
  - [ ] Show file paths and error messages
  - [ ] Suggest fixes for common issues

### 3.5 Additional CLI Commands

- [ ] Implement `config` command
  - [ ] Subcommand: `show` - display current config
  - [ ] Subcommand: `edit` - open config file in editor
  - [ ] Subcommand: `reset` - restore default config
- [ ] Implement `formats` command - list supported formats
- [ ] Implement `--gui` flag - launch GUI from CLI
- [ ] Add `--version` flag

### 3.6 CLI Testing

- [ ] Test all command options
- [ ] Test error handling (invalid paths, permissions)
- [ ] Test dry-run mode accuracy
- [ ] Test with various input scenarios

-----

## Phase 4: GUI Implementation

### 4.1 GUI Foundation

- [ ] Create `gui.py`
  - [ ] Set up main Tkinter window
  - [ ] Configure window properties (title, size, icon)
  - [ ] Implement responsive layout (grid/pack)
  - [ ] Set minimum window size
  - [ ] Handle window close event

### 4.2 Folder Selection

- [ ] Create folder selection frame
  - [ ] Folder path entry (readonly)
  - [ ] “Browse” button (opens folder dialog)
  - [ ] Recent folders dropdown (optional)
  - [ ] Drag-and-drop zone
    - [ ] Visual indicator for drop area
    - [ ] Handle drag-over events
    - [ ] Extract folder path from drop data
    - [ ] Validate dropped path is a folder
  - [ ] Recursive checkbox (scan subfolders)
  - [ ] Discovered images counter (updates on folder select)

### 4.3 Output Configuration

- [ ] Create output settings frame
  - [ ] Output directory entry
  - [ ] “Browse” button for output folder
  - [ ] Checkbox: “Use default location”
  - [ ] Filename pattern dropdown/entry

### 4.4 Conversion Options

- [ ] Create options frame
  - [ ] Format dropdown (WebP, JPEG, JPEG-XL, AVIF, PNG)
  - [ ] Quality slider (0-100) with numeric display
  - [ ] Lossless checkbox
  - [ ] Worker threads spinbox (1 to CPU count)
  - [ ] “Save as default” button

### 4.5 Preview Panel

- [ ] Create preview frame (two-column layout)
  - [ ] Before preview (original image)
    - [ ] Image display (scaled to fit)
    - [ ] File info (name, size, dimensions)
  - [ ] After preview (converted preview)
    - [ ] Simulated converted image
    - [ ] Estimated file size
    - [ ] Size reduction percentage
  - [ ] Select random sample image from batch for preview
  - [ ] “Refresh Preview” button

### 4.6 Action Buttons

- [ ] Create button frame
  - [ ] “Convert” button (primary action)
    - [ ] Validate inputs
    - [ ] Disable during processing
    - [ ] Launch conversion in background thread
  - [ ] “Stop” button (cancel processing)
  - [ ] “Clear” button (reset form)

### 4.7 Progress & Status

- [ ] Create progress frame
  - [ ] Progress bar (Tkinter.ttk.Progressbar)
  - [ ] Status label (current file being processed)
  - [ ] Progress percentage
  - [ ] Processing stats (speed, ETA)
  - [ ] Success/failure counters (live update)

### 4.8 Results & Logging

- [ ] Create results frame (tabs or collapsible)
  - [ ] Tab 1: Conversion log
    - [ ] Scrollable text widget
    - [ ] Color-coded messages (success=green, error=red)
    - [ ] Timestamps
  - [ ] Tab 2: Failed files list
    - [ ] Scrollable listbox
    - [ ] Error descriptions
    - [ ] “Export report” button (save to text file)
  - [ ] “Clear log” button

### 4.9 Menu Bar

- [ ] Create menu bar
  - [ ] File menu
    - [ ] “Select Folder”
    - [ ] “Open Output Folder”
    - [ ] “Exit”
  - [ ] Edit menu
    - [ ] “Settings/Preferences”
    - [ ] “Reset to defaults”
  - [ ] Help menu
    - [ ] “Documentation” (open README)
    - [ ] “About”

### 4.10 Threading & Concurrency

- [ ] Implement background processing
  - [ ] Create worker thread for batch conversion
  - [ ] Use queue for progress updates
  - [ ] Update UI from main thread (thread-safe)
  - [ ] Handle cancellation gracefully
  - [ ] Re-enable UI after completion

### 4.11 GUI Styling

- [ ] Apply consistent theming
  - [ ] Font sizes and families
  - [ ] Color scheme
  - [ ] Padding and spacing
  - [ ] Button styles
- [ ] Test on both macOS and Windows
  - [ ] Adjust for platform-specific quirks
  - [ ] Test high-DPI displays

### 4.12 GUI Testing

- [ ] Test all UI interactions
- [ ] Test drag-and-drop functionality
- [ ] Test progress updates
- [ ] Test cancellation
- [ ] Test error handling in GUI context
- [ ] Test with large batches (UI responsiveness)

-----

## Phase 5: Error Handling & Robustness

### 5.1 Input Validation

- [ ] Validate all user inputs (CLI and GUI)
  - [ ] Check paths exist and are accessible
  - [ ] Validate quality values (0-100)
  - [ ] Validate worker count (1 to CPU count)
  - [ ] Check output directory is writable
  - [ ] Verify supported formats

### 5.2 Error Collection

- [ ] Create `utils/logger.py`
  - [ ] Implement error collector class
  - [ ] Categorize errors (file not found, permission denied, conversion failed, etc.)
  - [ ] Store error context (file path, error message, timestamp)
  - [ ] Generate error reports (text, JSON, CSV)

### 5.3 Graceful Degradation

- [ ] Handle missing dependencies
  - [ ] Detect if JPEG-XL plugin not available
  - [ ] Detect if HEIF support missing
  - [ ] Show warning and disable unavailable formats
- [ ] Handle disk space issues
  - [ ] Check available disk space before conversion
  - [ ] Handle mid-conversion disk full errors
  - [ ] Clean up partial files
- [ ] Handle memory constraints
  - [ ] Catch memory errors during large image processing
  - [ ] Reduce worker count automatically if needed

### 5.4 Logging

- [ ] Set up Python logging module
  - [ ] Console logging (CLI)
  - [ ] File logging (optional, for debugging)
  - [ ] Configurable log levels
  - [ ] Rotate log files

-----

## Phase 6: Testing

### 6.1 Unit Tests

- [ ] Test `validator.py`
  - [ ] Valid PNG files
  - [ ] Invalid/corrupted files
  - [ ] Non-PNG files with .png extension
- [ ] Test `converter.py`
  - [ ] Each output format
  - [ ] Lossless vs lossy
  - [ ] Quality settings
  - [ ] Metadata preservation
  - [ ] Transparency handling
- [ ] Test `processor.py`
  - [ ] File discovery
  - [ ] Batch processing
  - [ ] Multiprocessing
  - [ ] Error collection
- [ ] Test `config.py`
  - [ ] Config loading
  - [ ] Default values
  - [ ] Validation

### 6.2 Integration Tests

- [ ] End-to-end CLI tests
  - [ ] Test conversion with various options
  - [ ] Test dry-run mode
  - [ ] Test verbose output
- [ ] End-to-end GUI tests (if possible with tkinter)
  - [ ] Test button clicks
  - [ ] Test folder selection
  - [ ] Test conversion process

### 6.3 Test Data

- [ ] Create test image set
  - [ ] Small images (< 100KB)
  - [ ] Medium images (100KB - 1MB)
  - [ ] Large images (> 1MB)
  - [ ] Images with transparency
  - [ ] Images with EXIF data
  - [ ] Images without EXIF data
  - [ ] Corrupted PNG file
  - [ ] Non-PNG with .png extension

### 6.4 Performance Testing

- [ ] Benchmark with different batch sizes
- [ ] Benchmark with different worker counts
- [ ] Memory usage profiling
- [ ] Identify and fix bottlenecks

-----

## Phase 7: Documentation

### 7.1 Code Documentation

- [ ] Add docstrings to all functions and classes
  - [ ] Parameter descriptions
  - [ ] Return value descriptions
  - [ ] Example usage
- [ ] Add inline comments for complex logic
- [ ] Type hints throughout codebase

### 7.2 User Documentation

- [ ] Update README.md
  - [ ] Project description and features
  - [ ] Installation instructions
  - [ ] CLI usage examples
  - [ ] GUI usage guide
  - [ ] Configuration guide
  - [ ] Troubleshooting section
- [ ] Create CONTRIBUTING.md
  - [ ] Development setup
  - [ ] Code style guide
  - [ ] Testing requirements
  - [ ] Pull request process
- [ ] Create CHANGELOG.md
  - [ ] Version history
  - [ ] Feature additions
  - [ ] Bug fixes

### 7.3 API Documentation

- [ ] Generate API docs (Sphinx or mkdocs)
  - [ ] Document core modules
  - [ ] Document utils modules
  - [ ] Include examples

-----

## Phase 8: Packaging & Distribution

### 8.1 UV Tool Configuration

- [ ] Configure `pyproject.toml` for UV tool installation
  - [ ] Define `[tool.uv]` section
  - [ ] Set up `[project.scripts]` entry points
    - [ ] `imageconverter = "imageconverter.gui:main"`
    - [ ] `imgconvert = "imageconverter.cli:main"`
- [ ] Test installation with `uv tool install .`
- [ ] Verify commands work globally

### 8.2 Platform-Specific Testing

- [ ] Test on macOS
  - [ ] Installation
  - [ ] CLI functionality
  - [ ] GUI appearance and behavior
  - [ ] File dialogs
- [ ] Test on Windows
  - [ ] Installation
  - [ ] CLI functionality
  - [ ] GUI appearance and behavior
  - [ ] File dialogs
  - [ ] Path handling (backslashes)

### 8.3 Release Preparation

- [ ] Version bumping strategy
- [ ] Create GitHub release workflow
- [ ] Tag releases properly
- [ ] Generate release notes

### 8.4 Distribution

- [ ] Publish to PyPI (optional)
  - [ ] Set up PyPI account
  - [ ] Configure authentication
  - [ ] Build distribution files
  - [ ] Upload to PyPI
- [ ] Create installation one-liner
  
  ```bash
  uv tool install imageconverter
  ```

-----

## Phase 9: Polish & Optimization

### 9.1 Performance Optimization

- [ ] Profile code to find bottlenecks
- [ ] Optimize image loading/saving
- [ ] Optimize multiprocessing overhead
- [ ] Cache configuration reads

### 9.2 UX Improvements

- [ ] Add keyboard shortcuts (GUI)
- [ ] Add tooltips to GUI elements
- [ ] Improve error messages (more actionable)
- [ ] Add confirmation dialogs for destructive actions

### 9.3 Edge Cases

- [ ] Handle extremely large images (> 50MB)
- [ ] Handle images with unusual color modes
- [ ] Handle write-protected output directories
- [ ] Handle network-mounted directories (slower I/O)

### 9.4 Code Quality

- [ ] Run black formatter on entire codebase
- [ ] Run ruff linter and fix issues
- [ ] Run mypy and add missing type hints
- [ ] Remove dead code
- [ ] Refactor duplicated code

-----

## Phase 10: Future Enhancements (Post-MVP)

### 10.1 Advanced Features

- [ ] Batch rename functionality
- [ ] Image resizing options (maintain aspect ratio)
- [ ] Watermarking support
- [ ] Watch folder mode (auto-convert on file add)

### 10.2 Cloud Integration

- [ ] Support for cloud storage (S3, GCS, Azure)
- [ ] Remote folder processing

### 10.3 Plugin System

- [ ] Design plugin architecture
- [ ] Allow custom format converters
- [ ] Allow custom preprocessing filters

### 10.4 Web Interface

- [ ] REST API for conversion service
- [ ] Web-based GUI (Flask/FastAPI + HTML frontend)

-----

## Milestone Checklist

- [ ] **Milestone 1:** Project setup complete, dependencies installed
- [ ] **Milestone 2:** Core converter working with one format (WebP)
- [ ] **Milestone 3:** CLI functional with basic options
- [ ] **Milestone 4:** Multiprocessing and batch processing working
- [ ] **Milestone 5:** All formats supported and tested
- [ ] **Milestone 6:** GUI functional with basic features
- [ ] **Milestone 7:** GUI complete with all features
- [ ] **Milestone 8:** Comprehensive tests passing
- [ ] **Milestone 9:** Documentation complete
- [ ] **Milestone 10:** Published and installable via UV

-----

## Notes for Implementation

### Priority Order

1. Core converter (Phase 2)
1. CLI (Phase 3)
1. GUI (Phase 4)
1. Testing & Documentation (Phases 6-7)
1. Distribution (Phase 8)

### Development Tips

- Start with WebP only, then add other formats
- Test CLI thoroughly before moving to GUI
- Use test-driven development for core modules
- Keep GUI and core logic separate (easier to test)
- Use type hints from the start (easier to maintain)

### Common Pitfalls to Avoid

- Don’t block the GUI thread with heavy processing
- Don’t forget to handle worker exceptions in multiprocessing
- Don’t assume file extensions match actual formats
- Don’t forget platform-specific path handling
- Test with large batches early (performance issues)