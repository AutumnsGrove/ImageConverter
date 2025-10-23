# Project Instructions - ImageConverter

> **Note**: This is the main orchestrator file. For detailed guides, see `ClaudeUsage/README.md`

---

## Project Purpose
ImageConverter is a cross-platform batch image conversion tool with CLI and GUI interfaces, optimized for converting PNG images to modern formats (WebP, JPEG-XL, AVIF, etc.) with metadata preservation and multiprocessing support.

## Tech Stack
- **Language**: Python 3.10+
- **Package Manager**: UV
- **Image Processing**: Pillow (PIL), pillow-heif
- **CLI Framework**: Click
- **GUI Framework**: Tkinter (built-in)
- **Progress Display**: Rich
- **Key Libraries**:
  - Pillow for image conversion
  - pillow-heif for AVIF/HEIF support
  - Click for CLI argument parsing
  - Rich for beautiful terminal output

## Architecture Notes
- **Separation of Concerns**: Core conversion logic is separate from CLI/GUI interfaces
- **Multiprocessing**: Batch processing uses concurrent.futures for parallel image conversion
- **Entry Points**: Two commands via pyproject.toml scripts:
  - `imageconverter` → GUI (imageconverter.gui:main)
  - `imgconvert` → CLI (imageconverter.cli:main)
- **Module Structure**:
  - `core/` - Conversion engine, validation, batch processing, config
  - `utils/` - Metadata handling, logging, path utilities
  - Entry points in root: `cli.py`, `gui.py`

---

## Essential Instructions (Always Follow)

### Core Behavior
- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary for achieving your goal
- ALWAYS prefer editing existing files to creating new ones
- NEVER proactively create documentation files (*.md) or README files unless explicitly requested

### Naming Conventions
- **Directories**: Use CamelCase (e.g., `VideoProcessor`, `AudioTools`, `DataAnalysis`)
- **Date-based paths**: Use skewer-case with YYYY-MM-DD (e.g., `logs-2025-01-15`, `backup-2025-12-31`)
- **No spaces or underscores** in directory names (except date-based paths)

### TODO Management
- **Always check `TODOS_REAL.md` first** when starting a task or session
- **Update immediately** when tasks are completed, added, or changed
- Keep the list current and manageable
- TODOS_REAL.md contains the comprehensive implementation plan

### Git Workflow Essentials
**After completing major changes, you MUST:**
1. Check git status: `git status`
2. Review recent commits for style: `git log --oneline -5`
3. Stage changes: `git add .`
4. Commit with proper message format (see below)

**Commit Message Format:**
```
[Action] [Brief description]

- [Specific change 1 with technical detail]
- [Specific change 2 with technical detail]
- [Additional implementation details]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Action Verbs**: Add, Update, Fix, Refactor, Remove, Enhance

---

## When to Read Specific Guides

**Read the full guide in `ClaudeUsage/` when you encounter these situations:**

### Secrets & API Keys
- **When managing API keys or secrets** → Read `ClaudeUsage/secrets_management.md`
- **Before implementing secrets loading** → Read `ClaudeUsage/secrets_management.md`

### Package Management
- **When using UV package manager** → Read `ClaudeUsage/uv_usage.md`
- **Before creating pyproject.toml** → Read `ClaudeUsage/uv_usage.md`
- **When managing Python dependencies** → Read `ClaudeUsage/uv_usage.md`

### Version Control
- **Before making a git commit** → Read `ClaudeUsage/git_commit_guide.md`
- **When initializing a new repo** → Read `ClaudeUsage/git_commit_guide.md`
- **For git workflow details** → Read `ClaudeUsage/git_commit_guide.md`

### Search & Research
- **When searching across 20+ files** → Read `ClaudeUsage/house_agents.md`
- **When finding patterns in codebase** → Read `ClaudeUsage/house_agents.md`
- **When locating TODOs/FIXMEs** → Read `ClaudeUsage/house_agents.md`

### Testing
- **Before writing tests** → Read `ClaudeUsage/testing_strategies.md`
- **When implementing test coverage** → Read `ClaudeUsage/testing_strategies.md`
- **For test organization** → Read `ClaudeUsage/testing_strategies.md`


### Code Quality
- **When refactoring code** → Read `ClaudeUsage/code_style_guide.md`
- **Before major code changes** → Read `ClaudeUsage/code_style_guide.md`
- **For style guidelines** → Read `ClaudeUsage/code_style_guide.md`

### Project Setup
- **When starting a new project** → Read `ClaudeUsage/project_setup.md`
- **For directory structure** → Read `ClaudeUsage/project_setup.md`
- **Setting up CI/CD** → Read `ClaudeUsage/project_setup.md`

---

## Quick Reference

### ImageConverter Specifics
- **Default Output**: `~/Downloads/ImageConverter_Output/`
- **Supported Formats**: WebP, JPEG, JPEG-XL, AVIF, PNG (optimized)
- **Default Quality**: 85 (lossy), 100 (lossless)
- **Config Location**:
  - macOS/Linux: `~/.config/imageconverter/config.yaml`
  - Windows: `%APPDATA%/imageconverter/config.yaml`

### Development Commands
```bash
# Install dependencies
uv sync

# Run CLI (development mode)
uv run imgconvert /path/to/images --format webp

# Run GUI (development mode)
uv run imageconverter

# Run tests
uv run pytest

# Code formatting
uv run black src/

# Linting
uv run ruff check src/

# Type checking
uv run mypy src/
```

### Security Basics
- No API keys required for core functionality
- If adding cloud features, store keys in `secrets.json` (NEVER commit)
- Add `secrets.json` to `.gitignore` immediately
- Provide `secrets_template.json` for setup
- Use environment variables as fallbacks


### House Agents Quick Trigger
**When searching 20+ files**, use house-research for:
- Finding patterns across codebase
- Searching TODO/FIXME comments
- Locating API endpoints or functions
- Documentation searches

---

## Code Style Guidelines

### Function & Variable Naming
- Use meaningful, descriptive names
- Keep functions small and focused on single responsibilities
- Add docstrings to all functions and classes
- Use type hints throughout

### Error Handling
- Use try/except blocks gracefully
- Provide helpful error messages
- Never let errors fail silently
- Collect errors during batch processing (don't stop on first failure)

### File Organization
- Group related functionality into modules
- Use consistent import ordering:
  1. Standard library
  2. Third-party packages
  3. Local imports
- Keep configuration separate from logic
- Keep GUI/CLI separate from core logic (for testability)

---

## Communication Style
- Be concise but thorough
- Explain reasoning for significant decisions
- Ask for clarification when requirements are ambiguous
- Proactively suggest improvements when appropriate

---

## Implementation Notes

### Pillow Image Conversion Pattern
```python
from PIL import Image

# Load image
img = Image.open(input_path)

# Convert with options
img.save(
    output_path,
    format="WEBP",
    quality=85,
    lossless=False,
    exif=img.info.get("exif"),  # Preserve metadata
)
```

### Multiprocessing Pattern
```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=workers) as executor:
    results = executor.map(convert_image, image_list)
```

### Progress Display Pattern (Rich)
```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("[green]Converting...", total=len(images))
    for result in results:
        progress.update(task, advance=1)
```

---

## Complete Guide Index
For all detailed guides, workflows, and examples, see:
**`ClaudeUsage/README.md`** - Master index of all documentation

---

*Last updated: 2025-10-23*
*Model: Claude Sonnet 4.5*
