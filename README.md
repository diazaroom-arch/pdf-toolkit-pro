# 🚀 PDF Toolkit Pro

> Professional command-line toolkit for PDF manipulation and automation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 What is PDF Toolkit Pro?

PDF Toolkit Pro is a powerful, production-ready command-line tool designed to automate PDF operations at scale. Built for developers, QA teams, and businesses that need to process hundreds or thousands of PDFs efficiently.

**Stop wasting time with manual PDF operations.** Automate everything.

## ✨ Features

- ✅ **Merge** multiple PDFs into one document
- ✅ **Split** PDFs by pages, ranges, or into individual pages
- ✅ **Extract** specific pages from any PDF
- ✅ **Add bookmarks** automatically when merging
- ✅ **Batch process** entire directories
- ✅ **Progress bars** for long operations
- ✅ **Detailed logging** and error handling
- ✅ **Cross-platform** (Windows, macOS, Linux)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-toolkit-pro.git
cd pdf-toolkit-pro

# Install in development mode
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

### Basic Usage

```bash
# Merge PDFs
pdf-toolkit merge file1.pdf file2.pdf file3.pdf -o combined.pdf

# Split PDF every 10 pages
pdf-toolkit split large_document.pdf --pages 10

# Extract specific pages
pdf-toolkit extract document.pdf --pages 1,5,10-15 -o selection.pdf

# Get PDF info
pdf-toolkit info document.pdf
```

## 📖 Detailed Usage

### Merge Operations

#### Merge multiple files
```bash
pdf-toolkit merge report1.pdf report2.pdf report3.pdf -o final_report.pdf
```

#### Merge all PDFs in a directory
```bash
pdf-toolkit merge-dir /path/to/pdfs/ -o combined.pdf
```

#### Merge with bookmarks (table of contents)
```bash
pdf-toolkit merge chapter*.pdf -o book.pdf --bookmarks
```

#### Merge recursively (including subdirectories)
```bash
pdf-toolkit merge-dir /documents/ -o all_docs.pdf --recursive
```

### Split Operations

#### Split every N pages
```bash
# Create files with 10 pages each
pdf-toolkit split document.pdf --pages 10
```

#### Split at specific page numbers
```bash
# Split at pages 25 and 50
pdf-toolkit split-at document.pdf --at 25 --at 50

# Result: 3 files (pages 1-24, 25-49, 50-end)
```

#### Split into individual pages
```bash
# Extract every page as a separate PDF
pdf-toolkit split-pages document.pdf --output-dir ./pages/
```

#### Custom output patterns
```bash
pdf-toolkit split doc.pdf -p 5 --pattern "section_{num}.pdf"
# Creates: section_1.pdf, section_2.pdf, ...
```

### Extract Operations

```bash
# Extract pages 1, 5, and 10-15
pdf-toolkit extract document.pdf --pages 1,5,10-15 -o selection.pdf

# Extract first 10 pages
pdf-toolkit extract document.pdf --pages 1-10 -o intro.pdf
```

### Information

```bash
# Get detailed info about a PDF
pdf-toolkit info document.pdf

# Output:
# 📄 PDF Information: document.pdf
#   Path:       /full/path/to/document.pdf
#   Size:       2.5 MB
#   Pages:      150
#   Metadata:
#     Title:    Sample Document
#     Author:   John Doe
```

## 🎯 Use Cases

### For Developers
- Automate report generation
- Batch process PDF exports
- Create test datasets
- Build PDF processing pipelines

### For QA Teams
- Generate test documentation
- Combine test result PDFs
- Extract specific test cases
- Organize test artifacts

### For Businesses
- Merge invoice batches
- Split large contracts
- Organize documentation
- Process form submissions
- Archive management

## 🛠️ Technical Details

### Architecture

```
pdf-toolkit-pro/
├── src/pdf_toolkit/
│   ├── cli.py           # Command-line interface
│   ├── merge.py         # Merge operations
│   ├── split.py         # Split operations
│   ├── extract.py       # Page extraction
│   ├── utils.py         # Common utilities
│   └── config.py        # Configuration
├── tests/               # Unit tests
└── examples/            # Usage examples
```

### Tech Stack

- **Python 3.8+** - Modern Python features
- **pypdf** - PDF manipulation library
- **Click** - Beautiful CLI framework
- **tqdm** - Progress bars
- **Pillow** - Image processing (for future features)
- **pytest** - Testing framework

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pdf_toolkit

# Run specific test file
pytest tests/test_merge.py
```

## 📦 Advanced Options

### Overwrite Protection

By default, PDF Toolkit Pro won't overwrite existing files:

```bash
# This will fail if output.pdf exists
pdf-toolkit merge *.pdf -o output.pdf

# Use --overwrite to force
pdf-toolkit merge *.pdf -o output.pdf --overwrite
```

### Progress Bars

```bash
# Disable progress bar for scripts/automation
pdf-toolkit merge *.pdf -o output.pdf --no-progress
```

### Logging

```bash
# Set log level via environment variable
export PDF_TOOLKIT_LOG_LEVEL=DEBUG
pdf-toolkit merge *.pdf -o output.pdf
```

## 🚧 Roadmap

- [ ] PDF compression
- [ ] Watermark addition
- [ ] Image to PDF conversion
- [ ] OCR text extraction
- [ ] PDF encryption/decryption
- [ ] Metadata editing
- [ ] Page rotation
- [ ] Web API interface

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Author

Created by **Aroom Diaz Neyra**

- GitHub: [@Aroom Díaz](https://github.com/diazaroom-arch)
- Email: diazneyraaroom@gmail.com

## 🙏 Acknowledgments

- Built with [pypdf](https://github.com/py-pdf/pypdf)
- CLI powered by [Click](https://click.palletsprojects.com/)
- Inspired by the need for better PDF automation

---

**⭐ If you find this useful, please star the repository!**

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/pdf-toolkit-pro?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/pdf-toolkit-pro?style=social)

## 🔥 Examples in Action

### Batch Processing
```bash
# Process 100 PDFs in seconds
for file in invoices/*.pdf; do
    pdf-toolkit split "$file" --pages 1
done
```

### Automation Script
```python
import os
from pdf_toolkit import merge_pdfs

# Merge all monthly reports
reports = [f"report_{i}.pdf" for i in range(1, 13)]
merge_pdfs(reports, "annual_report.pdf")
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Merge documentation
  run: |
    pdf-toolkit merge-dir docs/ -o documentation.pdf
```

## 📞 Support

Having issues? Check out:
- [Issues](https://github.com/yourusername/pdf-toolkit-pro/issues)
- [Discussions](https://github.com/yourusername/pdf-toolkit-pro/discussions)
- Email: diazneyraaroom@gmail.com

---

**Made with ❤️ and Python**
