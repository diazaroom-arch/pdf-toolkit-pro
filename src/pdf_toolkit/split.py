"""
PDF Toolkit Pro - Split Module
Split PDF files into multiple documents
"""

from pathlib import Path
from typing import List, Optional
from pypdf import PdfWriter, PdfReader
from tqdm import tqdm

from .utils import (
    validate_pdf_file,
    validate_output_path,
    format_file_size,
    print_success,
    print_info,
    logger
)


def split_by_pages(
    input_file: str,
    pages_per_split: int,
    output_pattern: str = "{base}_{num}.pdf",
    overwrite: bool = False,
    show_progress: bool = True
) -> List[Path]:
    """
    Split PDF into multiple files with specified pages per file.
    
    Args:
        input_file: Input PDF file path
        pages_per_split: Number of pages per output file
        output_pattern: Pattern for output files
                       {base} = original filename without extension
                       {num} = split number (1, 2, 3, ...)
        overwrite: Whether to overwrite existing files
        show_progress: Whether to show progress bar
        
    Returns:
        List of created PDF file paths
        
    Example:
        >>> split_by_pages('doc.pdf', pages_per_split=10)
        [Path('doc_1.pdf'), Path('doc_2.pdf'), ...]
    """
    # Validation
    input_path = validate_pdf_file(input_file)
    
    if pages_per_split < 1:
        raise ValueError("pages_per_split must be at least 1")
    
    # Read input PDF
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    
    print_info(
        f"Splitting {input_path.name} ({total_pages} pages) "
        f"into files of {pages_per_split} pages each"
    )
    
    # Calculate number of output files
    num_splits = (total_pages + pages_per_split - 1) // pages_per_split
    
    output_files = []
    
    # Progress bar
    progress = tqdm(
        range(num_splits),
        desc="Splitting",
        unit="file",
        disable=not show_progress
    )
    
    try:
        for split_num in progress:
            # Calculate page range for this split
            start_page = split_num * pages_per_split
            end_page = min(start_page + pages_per_split, total_pages)
            
            # Create output filename
            output_name = output_pattern.format(
                base=input_path.stem,
                num=split_num + 1
            )
            output_path = input_path.parent / output_name
            
            # Validate output path
            output_path = validate_output_path(str(output_path), overwrite)
            
            # Create PDF writer for this split
            writer = PdfWriter()
            
            # Add pages to this split
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            # Write output file
            with open(output_path, 'wb') as output:
                writer.write(output)
            
            output_files.append(output_path)
            
            file_size = output_path.stat().st_size
            logger.debug(
                f"Created {output_path.name}: "
                f"pages {start_page + 1}-{end_page} "
                f"({format_file_size(file_size)})"
            )
        
        print_success(
            f"Split into {len(output_files)} files "
            f"({pages_per_split} pages each)"
        )
        
        return output_files
        
    except Exception as e:
        logger.error(f"Error during split: {e}")
        raise


def split_at_pages(
    input_file: str,
    split_points: List[int],
    output_pattern: str = "{base}_part{num}.pdf",
    overwrite: bool = False
) -> List[Path]:
    """
    Split PDF at specific page numbers.
    
    Args:
        input_file: Input PDF file path
        split_points: List of page numbers where splits should occur
                     (1-indexed, e.g., [5, 10] creates 3 files:
                      pages 1-4, 5-9, 10-end)
        output_pattern: Pattern for output files
        overwrite: Whether to overwrite existing files
        
    Returns:
        List of created PDF file paths
        
    Example:
        >>> split_at_pages('doc.pdf', [10, 20])
        [Path('doc_part1.pdf'), Path('doc_part2.pdf'), Path('doc_part3.pdf')]
    """
    # Validation
    input_path = validate_pdf_file(input_file)
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    
    if not split_points:
        raise ValueError("No split points provided")
    
    # Validate split points
    split_points = sorted(set(split_points))
    for point in split_points:
        if point < 1 or point > total_pages:
            raise ValueError(
                f"Invalid split point: {point}. "
                f"Must be between 1 and {total_pages}"
            )
    
    print_info(
        f"Splitting {input_path.name} at pages: "
        f"{', '.join(map(str, split_points))}"
    )
    
    # Create ranges
    ranges = []
    start = 0
    
    for point in split_points:
        ranges.append((start, point - 1))  # 0-indexed, exclusive end
        start = point - 1
    ranges.append((start, total_pages))
    
    output_files = []
    
    try:
        for part_num, (start, end) in enumerate(ranges, 1):
            # Create output filename
            output_name = output_pattern.format(
                base=input_path.stem,
                num=part_num
            )
            output_path = input_path.parent / output_name
            output_path = validate_output_path(str(output_path), overwrite)
            
            # Create PDF writer
            writer = PdfWriter()
            
            # Add pages
            for page_num in range(start, end):
                writer.add_page(reader.pages[page_num])
            
            # Write file
            with open(output_path, 'wb') as output:
                writer.write(output)
            
            output_files.append(output_path)
            
            file_size = output_path.stat().st_size
            logger.info(
                f"Created {output_path.name}: "
                f"pages {start + 1}-{end} "
                f"({format_file_size(file_size)})"
            )
        
        print_success(f"Split into {len(output_files)} files")
        
        return output_files
        
    except Exception as e:
        logger.error(f"Error during split: {e}")
        raise


def split_into_singles(
    input_file: str,
    output_dir: Optional[str] = None,
    output_pattern: str = "{base}_page{num}.pdf",
    overwrite: bool = False,
    show_progress: bool = True
) -> List[Path]:
    """
    Split PDF into individual pages.
    
    Args:
        input_file: Input PDF file path
        output_dir: Output directory (default: same as input file)
        output_pattern: Pattern for output files
        overwrite: Whether to overwrite existing files
        show_progress: Whether to show progress bar
        
    Returns:
        List of created PDF file paths
    """
    input_path = validate_pdf_file(input_file)
    reader = PdfReader(str(input_path))
    total_pages = len(reader.pages)
    
    # Determine output directory
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = input_path.parent
    
    print_info(
        f"Splitting {input_path.name} into {total_pages} individual pages"
    )
    
    output_files = []
    
    progress = tqdm(
        range(total_pages),
        desc="Extracting pages",
        unit="page",
        disable=not show_progress
    )
    
    try:
        for page_num in progress:
            # Create output filename
            output_name = output_pattern.format(
                base=input_path.stem,
                num=page_num + 1
            )
            output_path = out_dir / output_name
            output_path = validate_output_path(str(output_path), overwrite)
            
            # Create single-page PDF
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            
            # Write file
            with open(output_path, 'wb') as output:
                writer.write(output)
            
            output_files.append(output_path)
        
        print_success(f"Created {len(output_files)} individual page files")
        
        return output_files
        
    except Exception as e:
        logger.error(f"Error during split into singles: {e}")
        raise
