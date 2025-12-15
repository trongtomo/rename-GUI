"""
Batch Prefix Renamer
--------------------
Simple, lightweight GUI app to batch-rename files by replacing a prefix.

Features:
- Drag & choose folder (via dialog)
- Preview before applying
- Replace prefix with custom output
- Optional separator between new prefix and remaining name
- Minimal resource usage (Tkinter only)

Python version: 3.8+

MIT License – safe to upload to GitHub
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class BatchRenamer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Batch Prefix Renamer")
        self.geometry("700x420")
        self.resizable(False, False)

        self.folder_path = ""
        self.files = []

        self._build_ui()

    def _build_ui(self):
        # Folder selection
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="Select Folder", command=self.select_folder).pack(side="left")
        self.folder_label = ttk.Label(top, text="No folder selected")
        self.folder_label.pack(side="left", padx=10)

        # Options
        opts = ttk.Frame(self, padding=10)
        opts.pack(fill="x")

        ttk.Label(opts, text="Old Prefix:").grid(row=0, column=0, sticky="w")
        self.old_prefix = ttk.Entry(opts, width=20)
        self.old_prefix.grid(row=0, column=1, padx=5)

        ttk.Label(opts, text="New Prefix:").grid(row=0, column=2, sticky="w")
        self.new_prefix = ttk.Entry(opts, width=20)
        self.new_prefix.grid(row=0, column=3, padx=5)

        ttk.Label(opts, text="Separator:").grid(row=1, column=0, sticky="w")
        self.separator = ttk.Entry(opts, width=20)
        self.separator.insert(0, "")
        self.separator.grid(row=1, column=1, padx=5)

        ttk.Button(opts, text="Preview", command=self.preview).grid(row=1, column=3, sticky="e")

        # File preview
        preview_frame = ttk.Frame(self, padding=10)
        preview_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(preview_frame, columns=("old", "new"), show="headings")
        self.tree.heading("old", text="Original Name")
        self.tree.heading("new", text="New Name")
        self.tree.column("old", width=320)
        self.tree.column("new", width=320)
        self.tree.pack(fill="both", expand=True)

        # Apply button
        bottom = ttk.Frame(self, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Apply Rename", command=self.apply).pack(side="right")

    def select_folder(self):
        path = filedialog.askdirectory()
        if not path:
            return
        self.folder_path = path
        self.folder_label.config(text=path)
        self.files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        self.tree.delete(*self.tree.get_children())

    def preview(self):
        self.tree.delete(*self.tree.get_children())

        old = self.old_prefix.get()
        new = self.new_prefix.get()
        sep = self.separator.get()

        if not old:
            messagebox.showwarning("Warning", "Old prefix is required")
            return

        for name in self.files:
            if name.startswith(old):
                rest = name[len(old):]
                new_name = f"{new}{sep}{rest}"
                self.tree.insert("", "end", values=(name, new_name))

    def apply(self):
        if not self.tree.get_children():
            return

        for item in self.tree.get_children():
            old_name, new_name = self.tree.item(item, "values")
            old_path = os.path.join(self.folder_path, old_name)
            new_path = os.path.join(self.folder_path, new_name)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)

        messagebox.showinfo("Done", "Files renamed successfully")
        self.select_folder()


if __name__ == "__main__":
    app = BatchRenamer()
    app.mainloop()
