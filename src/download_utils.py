"""Utilities for handling file downloads with progress tracking."""

import logging
from pathlib import Path

from requests import Response

from src.managers.progress_manager import ProgressManager

from .config import LARGE_FILE_CHUNK_SIZE, THRESHOLDS


def get_chunk_size(file_size: int) -> int:
    """Determine the optimal chunk size based on the file size."""
    # Handle cases where file_size is unknown or invalid
    if file_size <= 0:
        return LARGE_FILE_CHUNK_SIZE
    
    for threshold, chunk_size in THRESHOLDS:
        if file_size < threshold:
            return chunk_size

    return LARGE_FILE_CHUNK_SIZE


def save_file_with_progress(
    response: Response,
    download_path: str,
    task: int,
    progress_manager: ProgressManager,
) -> None:
    """Save the file from the response to the specified path."""
    file_size = int(response.headers.get("Content-Length", -1))
    
    # Handle missing or invalid content-length
    if file_size <= 0:
        logging.warning(
            "Content length not provided in response headers. "
            "Downloading without progress tracking."
        )
        file_size = None

    chunk_size = get_chunk_size(file_size if file_size else 1024 * 1024)
    total_downloaded = 0

    with Path(download_path).open("wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk is not None:
                file.write(chunk)
                total_downloaded += len(chunk)
                
                # Only update progress if file_size is known
                if file_size and file_size > 0:
                    completed = (total_downloaded / file_size) * 100
                    progress_manager.update_task(task, completed=completed)
                else:
                    # Advance progress bar by chunk size if total size unknown
                    progress_manager.update_task(task, advance=len(chunk))
