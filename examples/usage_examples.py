"""
PDF Toolkit Pro - Usage Examples
Demonstrates how to use the toolkit programmatically
"""

from pathlib import Path
from pdf_toolkit import merge_pdfs, split_by_pages, merge_directory

# ============================================================================
# EXAMPLE 1: Basic Merge
# ============================================================================

def example_basic_merge():
    """Merge two PDF files"""
    print("\n=== Example 1: Basic Merge ===")
    
    files = ["document1.pdf", "document2.pdf"]
    output = "combined.pdf"
    
    try:
        result = merge_pdfs(files, output, overwrite=True)
        print(f"✓ Created: {result}")
    except Exception as e:
        print(f"✗ Error: {e}")


# ============================================================================
# EXAMPLE 2: Merge Multiple Files
# ============================================================================

def example_merge_multiple():
    """Merge all chapter PDFs into a book"""
    print("\n=== Example 2: Merge Multiple Files ===")
    
    # Generate list of chapter files
    chapters = [f"chapter_{i:02d}.pdf" for i in range(1, 11)]
    output = "complete_book.pdf"
    
    try:
        result = merge_pdfs(chapters, output, overwrite=True)
        print(f"✓ Created: {result}")
    except Exception as e:
        print(f"✗ Error: {e}")


# ============================================================================
# EXAMPLE 3: Merge Directory
# ============================================================================

def example_merge_directory():
    """Merge all PDFs in a directory"""
    print("\n=== Example 3: Merge Directory ===")
    
    directory = "./invoices/"
    output = "all_invoices.pdf"
    
    try:
        result = merge_directory(
            directory,
            output,
            recursive=False,  # Don't search subdirectories
            overwrite=True
        )
        print(f"✓ Created: {result}")
    except Exception as e:
        print(f"✗ Error: {e}")


# ============================================================================
# EXAMPLE 4: Split PDF
# ============================================================================

def example_split_pdf():
    """Split large PDF into smaller chunks"""
    print("\n=== Example 4: Split PDF ===")
    
    input_file = "large_document.pdf"
    pages_per_file = 10
    
    try:
        results = split_by_pages(
            input_file,
            pages_per_file,
            overwrite=True
        )
        print(f"✓ Created {len(results)} files:")
        for file in results:
            print(f"  - {file.name}")
    except Exception as e:
        print(f"✗ Error: {e}")


# ============================================================================
# EXAMPLE 5: Batch Processing
# ============================================================================

def example_batch_processing():
    """Process multiple PDFs in a loop"""
    print("\n=== Example 5: Batch Processing ===")
    
    # List of PDF files to process
    pdf_files = Path("./reports/").glob("*.pdf")
    
    for pdf_file in pdf_files:
        try:
            # Split each PDF into 5-page chunks
            results = split_by_pages(
                str(pdf_file),
                pages_per_split=5,
                output_pattern=f"{pdf_file.stem}_part{{num}}.pdf",
                overwrite=True
            )
            print(f"✓ Processed: {pdf_file.name} -> {len(results)} files")
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")


# ============================================================================
# EXAMPLE 6: Automation Script
# ============================================================================

def example_automation():
    """
    Real-world automation example:
    Organize monthly reports by combining all PDFs from each month
    """
    print("\n=== Example 6: Automation Script ===")
    
    import os
    from datetime import datetime
    
    reports_dir = Path("./monthly_reports/")
    output_dir = Path("./annual_reports/")
    output_dir.mkdir(exist_ok=True)
    
    # Group files by month
    files_by_month = {}
    
    for pdf_file in reports_dir.glob("*.pdf"):
        # Assume filename format: report_2024-01-15.pdf
        try:
            date_str = pdf_file.stem.split("_")[1]
            date = datetime.strptime(date_str, "%Y-%m-%d")
            month_key = date.strftime("%Y-%m")
            
            if month_key not in files_by_month:
                files_by_month[month_key] = []
            
            files_by_month[month_key].append(str(pdf_file))
        except:
            continue
    
    # Merge each month's reports
    for month, files in files_by_month.items():
        output = output_dir / f"report_{month}.pdf"
        
        try:
            merge_pdfs(files, str(output), overwrite=True)
            print(f"✓ {month}: Merged {len(files)} reports -> {output.name}")
        except Exception as e:
            print(f"✗ Error for {month}: {e}")


# ============================================================================
# EXAMPLE 7: Error Handling
# ============================================================================

def example_error_handling():
    """Demonstrate proper error handling"""
    print("\n=== Example 7: Error Handling ===")
    
    from pypdf import PdfReader
    
    files_to_merge = ["file1.pdf", "file2.pdf", "file3.pdf"]
    
    # Check if all files exist before merging
    missing_files = []
    for file in files_to_merge:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return
    
    # Check if files are valid PDFs
    for file in files_to_merge:
        try:
            reader = PdfReader(file)
            print(f"✓ {file}: {len(reader.pages)} pages")
        except Exception as e:
            print(f"✗ {file} is not a valid PDF: {e}")
            return
    
    # Now merge
    try:
        output = "combined.pdf"
        result = merge_pdfs(files_to_merge, output, overwrite=True)
        print(f"✓ Successfully created: {result}")
    except Exception as e:
        print(f"✗ Merge failed: {e}")


# ============================================================================
# EXAMPLE 8: Custom Workflow
# ============================================================================

def example_custom_workflow():
    """
    Custom workflow: 
    1. Split large PDF
    2. Process each part
    3. Merge back together
    """
    print("\n=== Example 8: Custom Workflow ===")
    
    original_file = "large_document.pdf"
    temp_dir = Path("./temp_processing/")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Step 1: Split into parts
        print("Step 1: Splitting...")
        parts = split_by_pages(
            original_file,
            pages_per_split=10,
            output_pattern=str(temp_dir / "part_{num}.pdf"),
            overwrite=True
        )
        print(f"  Created {len(parts)} parts")
        
        # Step 2: Process each part (placeholder for your processing)
        print("Step 2: Processing parts...")
        processed_parts = []
        for part in parts:
            # Here you could:
            # - Extract text
            # - Add watermarks
            # - Compress
            # - etc.
            processed_parts.append(str(part))
            print(f"  Processed: {part.name}")
        
        # Step 3: Merge back
        print("Step 3: Merging...")
        final_output = "processed_document.pdf"
        merge_pdfs(processed_parts, final_output, overwrite=True)
        print(f"✓ Created: {final_output}")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        print("✓ Cleaned up temporary files")
        
    except Exception as e:
        print(f"✗ Workflow failed: {e}")


# ============================================================================
# RUN EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("PDF Toolkit Pro - Usage Examples")
    print("=" * 50)
    
    # Uncomment the examples you want to run:
    
    # example_basic_merge()
    # example_merge_multiple()
    # example_merge_directory()
    # example_split_pdf()
    # example_batch_processing()
    # example_automation()
    # example_error_handling()
    # example_custom_workflow()
    
    print("\n" + "=" * 50)
    print("Uncomment examples in the code to run them")
