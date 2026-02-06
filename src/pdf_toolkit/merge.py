"""
PDF Toolkit Pro - Merge Module
Combine multiple PDF files into a single document
"""

from pathlib import Path
from typing import List, Optional
from pypdf import PdfWriter, PdfReader
from tqdm import tqdm

from .utils import (
    validate_pdf_file,
    validate_output_path,
    get_pdf_files,
    format_file_size,
    print_success,
    print_info,
    logger
)


def merge_pdfs(
    input_files: List[str],
    output_file: str,
    overwrite: bool = False,
    show_progress: bool = True
) -> Path:
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        input_files: List of input PDF file paths
        output_file: Output PDF file path
        overwrite: Whether to overwrite existing output file
        show_progress: Whether to show progress bar
        
    Returns:
        Path to the created PDF file
        
    Raises:
        FileNotFoundError: If any input file doesn't exist
        ValueError: If input list is empty or files are invalid
        FileExistsError: If output exists and overwrite is False
        
    Example:
        >>> merge_pdfs(['doc1.pdf', 'doc2.pdf'], 'combined.pdf')
        Path('combined.pdf')
    """
    # Validation
    if not input_files:
        raise ValueError("No input files provided")
    
    if len(input_files) < 2:
        raise ValueError("At least 2 PDF files are required for merging")
    
    # Validate all input files
    validated_files = [validate_pdf_file(f) for f in input_files]
    output_path = validate_output_path(output_file, overwrite)
    
    print_info(f"Merging {len(validated_files)} PDF files...")
    
    # Create PDF writer
    merger = PdfWriter()
    
    # Progress bar setup
    progress_bar = tqdm(
        validated_files,
        desc="Merging",
        unit="file",
        disable=not show_progress
    )
    
    try:
        total_pages = 0
        
        for pdf_file in progress_bar:
            progress_bar.set_postfix(file=pdf_file.name)
            
            # Read and append PDF
            reader = PdfReader(str(pdf_file))
            num_pages = len(reader.pages)
            
            for page in reader.pages:
                merger.add_page(page)
            
            total_pages += num_pages
            logger.debug(f"Added {pdf_file.name} ({num_pages} pages)")
        
        # Write output file
        print_info(f"Writing output file: {output_path.name}")
        with open(output_path, 'wb') as output:
            merger.write(output)
        
        # Get file size
        file_size = output_path.stat().st_size
        
        print_success(
            f"Merged {len(validated_files)} files "
            f"({total_pages} pages total) → {output_path.name} "
            f"({format_file_size(file_size)})"
        )
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error during merge: {e}")
        raise
    finally:
        merger.close()


def merge_directory(
    directory: str,
    output_file: str,
    recursive: bool = False,
    overwrite: bool = False,
    show_progress: bool = True
) -> Path:
    """
    Merge all PDF files in a directory.
    
    Args:
        directory: Directory containing PDF files
        output_file: Output PDF file path
        recursive: Whether to search subdirectories
        overwrite: Whether to overwrite existing output file
        show_progress: Whether to show progress bar
        
    Returns:
        Path to the created PDF file
        
    Example:
        >>> merge_directory('/path/to/pdfs', 'combined.pdf')
        Path('combined.pdf')
    """
    # Get all PDF files from directory
    pdf_files = get_pdf_files(directory, recursive)
    
    if not pdf_files:
        raise ValueError(f"No PDF files found in directory: {directory}")
    
    print_info(
        f"Found {len(pdf_files)} PDF file(s) in "
        f"{'directory tree' if recursive else 'directory'}"
    )
    
    # Convert to strings for merge_pdfs
    file_paths = [str(f) for f in pdf_files]
    
    return merge_pdfs(file_paths, output_file, overwrite, show_progress)


def merge_with_bookmarks(
    input_files: List[str],
    output_file: str,
    bookmark_titles: Optional[List[str]] = None,
    overwrite: bool = False
) -> Path:
    """
    Merge PDFs and add bookmarks for each original file.
    
    Args:
        input_files: List of input PDF file paths
        output_file: Output PDF file path
        bookmark_titles: Optional custom titles for bookmarks
                        (if None, uses filenames)
        overwrite: Whether to overwrite existing output file
        
    Returns:
        Path to the created PDF file
    """
    if not input_files:
        raise ValueError("No input files provided")
    
    # Validate files
    validated_files = [validate_pdf_file(f) for f in input_files]
    output_path = validate_output_path(output_file, overwrite)
    
    # Use filenames as bookmark titles if not provided
    if bookmark_titles is None:
        bookmark_titles = [f.stem for f in validated_files]
    elif len(bookmark_titles) != len(input_files):
        raise ValueError(
            f"Number of bookmark titles ({len(bookmark_titles)}) "
            f"doesn't match number of files ({len(input_files)})"
        )
    
    print_info(f"Merging {len(validated_files)} PDFs with bookmarks...")
    
    merger = PdfWriter()
    current_page = 0
    
    try:
        for pdf_file, title in zip(validated_files, bookmark_titles):
            reader = PdfReader(str(pdf_file))
            
            # Add bookmark at the start of this PDF
            merger.add_outline_item(title, current_page)
            
            # Add all pages
            for page in reader.pages:
                merger.add_page(page)
            
            current_page += len(reader.pages)
            logger.debug(f"Added {pdf_file.name} with bookmark '{title}'")
        
        # Write output
        with open(output_path, 'wb') as output:
            merger.write(output)
        
        file_size = output_path.stat().st_size
        print_success(
            f"Created {output_path.name} with {len(bookmark_titles)} bookmarks "
            f"({format_file_size(file_size)})"
        )
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error during merge with bookmarks: {e}")
        raise
    finally:
        merger.close()
