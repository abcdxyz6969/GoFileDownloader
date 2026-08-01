"""Utility functions for file input and output operations.

It includes methods to read the contents of a file and to write content to a file, with
optional support for clearing the file.
"""

from pathlib import Path
from typing import List

from .config import SESSION_LOG


def read_file(filename: str) -> List[str]:
    """Read the contents of a file and returns a list of its lines."""
    with Path(filename).open(encoding="utf-8") as file:
        return file.read().splitlines()


def write_file(filename: str, content: str = "") -> None:
    """Write content to a specified file.

    If content is not provided, the file is cleared.
    """
    with Path(filename).open("w", encoding="utf-8") as file:
        file.write(content)


def write_on_session_log(content: str) -> None:
    """Append content to the session log file."""
    with Path(SESSION_LOG).open("a", encoding="utf-8") as file:
        file.write(f"{content}\n")


def create_download_directory(directory_name: str) -> None:
    """Create a directory for saving files if it does not already exist."""
    filepath = Path.cwd() / Path(directory_name)
    filepath.mkdir(parents=True, exist_ok=True)
