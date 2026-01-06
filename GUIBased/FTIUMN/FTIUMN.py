import os
import tkinter as tk
from tkinter import filedialog, messagebox

MAGIC_NUMBERS = {
    "PDF": b"%PDF",
    "PNG": b"\x89PNG\r\n\x1a\n",
    "JPG": b"\xff\xd8\xff",
    "ZIP": b"PK\x03\x04",
    "EXE": b"MZ"
}

EXTENSION_MAP = {
    ".pdf": "PDF",
    ".png": "PNG",
    ".jpg": "JPG",
    ".jpeg": "JPG",
    ".zip": "ZIP",
    ".exe": "EXE"
}

def identify_file_type(file_path):
    with open(file_path, "rb") as f:
        header = f.read(8)

    for file_type, magic in MAGIC_NUMBERS.items():
        if header.startswith(magic):
            return file_type
    return "Unknown"

def select_file():
    file_path = filedialog.askopenfilename(title="Select a file to analyze")

    if not file_path:
        return

    actual_type = identify_file_type(file_path)
    extension = os.path.splitext(file_path)[1].lower()
    claimed_type = EXTENSION_MAP.get(extension, "Unknown")

    result = (
        f"File: {file_path}\n\n"
        f"Claimed Type (extension): {claimed_type}\n"
        f"Actual Type (magic number): {actual_type}\n\n"
    )

    if claimed_type != actual_type:
        result += "⚠️ Mismatch detected! Possible disguised file."
    else:
        result += "✅ File type matches."

    messagebox.showinfo("File Analysis Result", result)

# ---- GUI Setup ----
root = tk.Tk()
root.title("File Type Identifier")
root.geometry("300x150")
root.resizable(False, False)

btn = tk.Button(root, text="Select File", command=select_file, width=20, height=2)
btn.pack(expand=True)

root.mainloop()
