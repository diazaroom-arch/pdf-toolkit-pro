"""
PDF Toolkit Pro - Utilities
Common utility functions used across the application
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_pdf_file(filepath: str) -> Path:
    """
    Validate that a file exists and is a PDF.
    
    Args:
        filepath: Path to the PDF file
        
    Returns:
        Path object if valid
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a PDF
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    if not path.suffix.lower() == '.pdf':
        raise ValueError(f"Not a PDF file: {filepath}")
    
    return path


def validate_output_path(filepath: str, overwrite: bool = False) -> Path:
    """
    Validate output path and handle overwrite logic.
    
    Args:
        filepath: Desired output path
        overwrite: Whether to allow overwriting existing files
        
    Returns:
        Path object for output
        
    Raises:
        FileExistsError: If file exists and overwrite is False
    """
    path = Path(filepath)
    
    if path.exists() and not overwrite:
        raise FileExistsError(
            f"Output file already exists: {filepath}\n"
            f"Use --overwrite flag to replace it."
        )
    
    # Create parent directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    
    return path


def get_pdf_files(directory: str, recursive: bool = False) -> List[Path]:
    """
    Get all PDF files from a directory.
    
    Args:
        directory: Directory path
        recursive: Whether to search recursively
        
    Returns:
        List of PDF file paths
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    if not dir_path.is_dir():
        raise ValueError(f"Not a directory: {directory}")
    
    pattern = '**/*.pdf' if recursive else '*.pdf'
    pdf_files = list(dir_path.glob(pattern))
    
    return sorted(pdf_files)


def parse_page_ranges(range_string: str, total_pages: int) -> List[int]:
    """
    Parse page range string into list of page numbers.
    
    Examples:
        "1,3,5" -> [0, 2, 4]  (0-indexed)
        "1-5" -> [0, 1, 2, 3, 4]
        "1,3-5,10" -> [0, 2, 3, 4, 9]
        
    Args:
        range_string: Page range specification
        total_pages: Total number of pages in document
        
    Returns:
        List of 0-indexed page numbers
        
    Raises:
        ValueError: If range specification is invalid
    """
    pages = set()
    
    for part in range_string.split(','):
        part = part.strip()
        
        if '-' in part:
            # Handle range (e.g., "1-5")
            try:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                
                if start < 1 or end > total_pages or start > end:
                    raise ValueError(
                        f"Invalid range: {part}. "
                        f"Must be between 1 and {total_pages}"
                    )
                
                pages.update(range(start - 1, end))
                
            except ValueError as e:
                raise ValueError(f"Invalid range format: {part}") from e
        else:
            # Handle single page
            try:
                page = int(part)
                
                if page < 1 or page > total_pages:
                    raise ValueError(
                        f"Invalid page number: {page}. "
                        f"Must be between 1 and {total_pages}"
                    )
                
                pages.add(page - 1)
                
            except ValueError as e:
                raise ValueError(f"Invalid page number: {part}") from e
    
    return sorted(list(pages))


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def print_success(message: str):
    """Print success message in green."""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Print error message in red."""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}", file=sys.stderr)


def print_warning(message: str):
    """Print warning message in yellow."""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Print info message in blue."""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation.
    
    Args:
        message: Question to ask
        default: Default answer if user just presses Enter
        
    Returns:
        True if user confirms, False otherwise
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    
    while True:
        response = input(message + suffix).strip().lower()
        
        if not response:
            return default
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print_warning("Please answer 'y' or 'n'")
