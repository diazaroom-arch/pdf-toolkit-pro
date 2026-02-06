"""
PDF Toolkit Pro - Configuration
Central configuration for the application
"""

import os
from pathlib import Path

# Application metadata
APP_NAME = "PDF Toolkit Pro"
VERSION = "1.0.0"
AUTHOR = "Your Name"

# Directories
BASE_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# PDF Processing settings
DEFAULT_COMPRESSION_QUALITY = "medium"
COMPRESSION_LEVELS = {
    "low": 50,
    "medium": 75,
    "high": 90
}

# Watermark settings
DEFAULT_WATERMARK_OPACITY = 0.3
DEFAULT_WATERMARK_FONT_SIZE = 40
DEFAULT_WATERMARK_COLOR = (128, 128, 128)  # Gray

# Image to PDF settings
DEFAULT_IMAGE_QUALITY = 85
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

# Text extraction settings
DEFAULT_ENCODING = 'utf-8'

# Logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = os.getenv('PDF_TOOLKIT_LOG_LEVEL', 'INFO')

# Performance
MAX_WORKERS = 4  # For parallel processing
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for file operations
