"""
Tests for PDF merge functionality
"""

import pytest
from pathlib import Path
from pypdf import PdfWriter, PdfReader
import tempfile
import shutil

from pdf_toolkit.merge import merge_pdfs, merge_directory


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_pdfs(temp_dir):
    """Create sample PDF files for testing"""
    pdfs = []
    
    for i in range(3):
        pdf_path = temp_dir / f"sample_{i+1}.pdf"
        writer = PdfWriter()
        
        # Add 5 blank pages to each PDF
        for _ in range(5):
            writer.add_blank_page(width=612, height=792)
        
        with open(pdf_path, 'wb') as f:
            writer.write(f)
        
        pdfs.append(pdf_path)
    
    return pdfs


class TestMergePDFs:
    
    def test_merge_two_pdfs(self, sample_pdfs, temp_dir):
        """Test merging two PDF files"""
        output = temp_dir / "merged.pdf"
        
        result = merge_pdfs(
            [str(sample_pdfs[0]), str(sample_pdfs[1])],
            str(output),
            show_progress=False
        )
        
        assert result.exists()
        
        # Verify merged PDF has correct number of pages (5 + 5 = 10)
        reader = PdfReader(str(result))
        assert len(reader.pages) == 10
    
    def test_merge_three_pdfs(self, sample_pdfs, temp_dir):
        """Test merging three PDF files"""
        output = temp_dir / "merged_three.pdf"
        
        result = merge_pdfs(
            [str(p) for p in sample_pdfs],
            str(output),
            show_progress=False
        )
        
        assert result.exists()
        
        # Verify merged PDF has 15 pages (3 PDFs × 5 pages each)
        reader = PdfReader(str(result))
        assert len(reader.pages) == 15
    
    def test_merge_with_invalid_file(self, sample_pdfs, temp_dir):
        """Test that merge fails with non-existent file"""
        output = temp_dir / "merged.pdf"
        
        with pytest.raises(FileNotFoundError):
            merge_pdfs(
                [str(sample_pdfs[0]), "nonexistent.pdf"],
                str(output),
                show_progress=False
            )
    
    def test_merge_with_empty_list(self, temp_dir):
        """Test that merge fails with empty file list"""
        output = temp_dir / "merged.pdf"
        
        with pytest.raises(ValueError):
            merge_pdfs([], str(output), show_progress=False)
    
    def test_merge_single_file(self, sample_pdfs, temp_dir):
        """Test that merge requires at least 2 files"""
        output = temp_dir / "merged.pdf"
        
        with pytest.raises(ValueError):
            merge_pdfs([str(sample_pdfs[0])], str(output), show_progress=False)
    
    def test_merge_overwrite_false(self, sample_pdfs, temp_dir):
        """Test that merge doesn't overwrite by default"""
        output = temp_dir / "merged.pdf"
        
        # Create first merge
        merge_pdfs(
            [str(sample_pdfs[0]), str(sample_pdfs[1])],
            str(output),
            show_progress=False
        )
        
        # Try to merge again without overwrite flag
        with pytest.raises(FileExistsError):
            merge_pdfs(
                [str(sample_pdfs[0]), str(sample_pdfs[1])],
                str(output),
                overwrite=False,
                show_progress=False
            )
    
    def test_merge_with_overwrite(self, sample_pdfs, temp_dir):
        """Test that merge overwrites when flag is set"""
        output = temp_dir / "merged.pdf"
        
        # Create first merge (2 files = 10 pages)
        merge_pdfs(
            [str(sample_pdfs[0]), str(sample_pdfs[1])],
            str(output),
            show_progress=False
        )
        
        # Merge again with all 3 files (15 pages) and overwrite
        result = merge_pdfs(
            [str(p) for p in sample_pdfs],
            str(output),
            overwrite=True,
            show_progress=False
        )
        
        # Verify it was overwritten (should have 15 pages now)
        reader = PdfReader(str(result))
        assert len(reader.pages) == 15


class TestMergeDirectory:
    
    def test_merge_directory(self, sample_pdfs, temp_dir):
        """Test merging all PDFs in a directory"""
        output = temp_dir / "merged_dir.pdf"
        
        # All sample PDFs are in temp_dir
        result = merge_directory(
            str(temp_dir),
            str(output),
            show_progress=False
        )
        
        assert result.exists()
        
        # Should have 15 pages (3 PDFs × 5 pages)
        reader = PdfReader(str(result))
        assert len(reader.pages) == 15
    
    def test_merge_directory_empty(self, temp_dir):
        """Test that merge fails on directory with no PDFs"""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        output = temp_dir / "merged.pdf"
        
        with pytest.raises(ValueError):
            merge_directory(
                str(empty_dir),
                str(output),
                show_progress=False
            )
    
    def test_merge_directory_recursive(self, sample_pdfs, temp_dir):
        """Test recursive directory merge"""
        # Create subdirectory with additional PDF
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        
        # Create one more PDF in subdirectory
        sub_pdf = subdir / "sample_4.pdf"
        writer = PdfWriter()
        for _ in range(5):
            writer.add_blank_page(width=612, height=792)
        with open(sub_pdf, 'wb') as f:
            writer.write(f)
        
        output = temp_dir / "merged_recursive.pdf"
        
        result = merge_directory(
            str(temp_dir),
            str(output),
            recursive=True,
            show_progress=False
        )
        
        # Should have 20 pages (4 PDFs × 5 pages)
        reader = PdfReader(str(result))
        assert len(reader.pages) == 20


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
