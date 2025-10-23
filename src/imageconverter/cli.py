"""CLI interface for ImageConverter."""

import click
from rich.console import Console

console = Console()


@click.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.option("--format", default="webp", help="Output format (webp, jpeg, jpeg-xl, avif, png)")
@click.option("--quality", default=85, type=int, help="Quality setting (0-100)")
@click.option("--lossless", is_flag=True, help="Use lossless compression")
@click.option("--recursive/--no-recursive", default=True, help="Scan subfolders recursively")
@click.option("--output", type=click.Path(), help="Output directory")
@click.option("--workers", type=int, help="Number of worker threads")
@click.option("--dry-run", is_flag=True, help="Preview without converting")
@click.option("--verbose", is_flag=True, help="Verbose output")
@click.option("--filename-pattern", help="Filename pattern template")
def main(
    input_dir: str,
    format: str,
    quality: int,
    lossless: bool,
    recursive: bool,
    output: str | None,
    workers: int | None,
    dry_run: bool,
    verbose: bool,
    filename_pattern: str | None,
) -> None:
    """Convert PNG images to modern formats.

    INPUT_DIR: Directory containing PNG images to convert
    """
    console.print("[bold green]ImageConverter CLI[/bold green]")
    console.print(f"Input directory: {input_dir}")
    console.print(f"Format: {format}")
    console.print(f"Quality: {quality}")

    if dry_run:
        console.print("[yellow]DRY RUN MODE - No files will be converted[/yellow]")

    # TODO: Implement actual conversion logic
    console.print("[yellow]Conversion logic not yet implemented[/yellow]")


if __name__ == "__main__":
    main()
