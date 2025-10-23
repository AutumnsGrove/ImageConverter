"""GUI interface for ImageConverter using Tkinter."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class ImageConverterGUI:
    """Main GUI window for ImageConverter."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the GUI."""
        self.root = root
        self.root.title("ImageConverter")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

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

        # Convert button
        ttk.Button(
            main_frame, text="Convert Images", command=self._convert_images
        ).grid(row=3, column=1, pady=20)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(
            row=4, column=0, columnspan=3
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
        """Start image conversion process."""
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("No Folder", "Please select an input folder first.")
            return

        format_type = self.format_var.get()
        quality = self.quality_var.get()

        # TODO: Implement actual conversion logic
        self.status_var.set(
            f"Converting to {format_type} with quality {quality}... (Not implemented yet)"
        )
        messagebox.showinfo(
            "Not Implemented",
            "Conversion logic not yet implemented.\n\n"
            f"Would convert images in:\n{folder}\n"
            f"Format: {format_type}\n"
            f"Quality: {quality}",
        )


def main() -> None:
    """Launch the ImageConverter GUI."""
    root = tk.Tk()
    app = ImageConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
