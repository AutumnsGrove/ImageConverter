"""CLI interface for ImageConverter."""

import click
from pathlib import Path
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeRemainingColumn,
)

from .core.processor import BatchProcessor

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
        "format": format,
        "quality": quality,
        "lossless": lossless,
        "output_dir": str(output_path),
    }
    if filename_pattern:
        options["filename_pattern"] = filename_pattern

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Converting images...", total=len(images))

        def update_progress(current: int, total: int, filename: str = "") -> None:
            progress.update(
                task, completed=current, description=f"[cyan]Converting {filename}"
            )

        results = processor.process_batch(images, options, update_progress)

    # Show summary
    console.print(f"\n[bold green]Conversion Complete![/bold green]")
    console.print(f"Total: {results['total']}")
    console.print(f"[green]Successful: {results['successes']}[/green]")
    console.print(f"[red]Failed: {results['failures']}[/red]")

    if results["errors"]:
        console.print(f"\n[red]Errors:[/red]")
        for error in results["errors"][:10]:  # Show first 10 errors
            console.print(f"  {error['file']}: {error['error']}")
        if len(results["errors"]) > 10:
            console.print(f"  ... and {len(results['errors']) - 10} more errors")


if __name__ == "__main__":
    main()
