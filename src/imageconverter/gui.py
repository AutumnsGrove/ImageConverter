"""GUI interface for ImageConverter using Tkinter."""

import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox

from .core.processor import BatchProcessor


class ImageConverterGUI:
    """Main GUI window for ImageConverter."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the GUI."""
        self.root = root
        self.root.title("ImageConverter")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Processing state
        self.processor = BatchProcessor()
        self.processing = False
        self.cancel_processing = False

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Folder selection
        ttk.Label(main_frame, text="Input Folder:").grid(row=0, column=0, sticky=tk.W)
        self.folder_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.folder_path, width=50).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(main_frame, text="Browse", command=self._select_folder).grid(
            row=0, column=2
        )

        # Format selection
        ttk.Label(main_frame, text="Output Format:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="webp")
        format_combo = ttk.Combobox(
            main_frame,
            textvariable=self.format_var,
            values=["webp", "jpeg", "jpeg-xl", "avif", "png"],
            state="readonly",
        )
        format_combo.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Quality slider
        ttk.Label(main_frame, text="Quality:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.IntVar(value=85)
        quality_scale = ttk.Scale(
            main_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            length=300,
        )
        quality_scale.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Label(main_frame, textvariable=self.quality_var).grid(row=2, column=2)

        # Workers and lossless controls
        ttk.Label(main_frame, text="Workers:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.workers_var = tk.IntVar(value=4)
        workers_spin = ttk.Spinbox(
            main_frame, from_=1, to=16, textvariable=self.workers_var, width=10
        )
        workers_spin.grid(row=3, column=1, sticky=tk.W, padx=5)

        self.lossless_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Lossless", variable=self.lossless_var).grid(
            row=3, column=2, sticky=tk.W
        )

        # Convert button
        ttk.Button(
            main_frame, text="Convert Images", command=self._convert_images
        ).grid(row=4, column=1, pady=20)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(
            row=6, column=0, columnspan=3
        )

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def _select_folder(self) -> None:
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.folder_path.set(folder)
            self.status_var.set(f"Selected: {folder}")

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


def main() -> None:
    """Launch the ImageConverter GUI."""
    root = tk.Tk()
    app = ImageConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
