import os
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

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

def scan_file(file_path):
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Scanning file header..."),
        transient=True,
    ) as progress:
        task = progress.add_task("scan", total=100)
        for _ in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)

    actual = identify_file_type(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    claimed = EXTENSION_MAP.get(ext, "Unknown")

    result = f"""
[bold]File:[/bold] {file_path}

[bold]Claimed Type:[/bold] {claimed}
[bold]Actual Type:[/bold] {actual}
"""

    if claimed != actual:
        console.print(Panel(result + "\n[red]⚠ MISMATCH DETECTED[/red]", title="Result"))
    else:
        console.print(Panel(result + "\n[green]✔ File type matches[/green]", title="Result"))

# ---- CLI Entry ----
console.print("[bold green]File Type Identifier (Magic Numbers)[/bold green]\n")

file_path = Prompt.ask("Enter file path to scan")

if os.path.isfile(file_path):
    scan_file(file_path)
else:
    console.print("[red]File does not exist[/red]")

