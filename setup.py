from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-toolkit-pro",
    version="1.0.0",
    author="Your Name",
    author_email="your@email.com",
    description="Professional PDF manipulation toolkit for automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pdf-toolkit-pro",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pypdf>=4.0.0",
        "click>=8.0.0",
        "Pillow>=10.0.0",
        "tqdm>=4.60.0",
        "colorama>=0.4.0",
    ],
    extras_require={
        "ocr": ["pytesseract>=0.3.0"],
        "dev": ["pytest>=8.0.0", "pytest-cov>=4.0.0", "black>=24.0.0", "flake8>=7.0.0"],
    },
    entry_points={
        "console_scripts": [
            "pdf-toolkit=pdf_toolkit.cli:cli",
        ],
    },
)
