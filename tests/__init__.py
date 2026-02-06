"""
PDF Toolkit Pro
Professional PDF manipulation toolkit for automation

Author: Your Name
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from .merge import merge_pdfs, merge_directory, merge_with_bookmarks
from .split import split_by_pages, split_at_pages, split_into_singles

__all__ = [
    'merge_pdfs',
    'merge_directory',
    'merge_with_bookmarks',
    'split_by_pages',
    'split_at_pages',
    'split_into_singles',
]
