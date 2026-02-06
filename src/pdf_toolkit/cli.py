"""
PDF Toolkit Pro - Command Line Interface
Professional CLI for PDF manipulation
"""

import click
from pathlib import Path
import sys

from . import __version__
from .merge import merge_pdfs, merge_directory, merge_with_bookmarks
from .split import split_by_pages, split_at_pages, split_into_singles
from .utils import print_error, print_info, confirm_action


# Custom Click group with better help formatting
class CustomGroup(click.Group):
    def format_help(self, ctx, formatter):
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_commands(ctx, formatter)
    
    def format_commands(self, ctx, formatter):
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help_text = cmd.get_short_help_str(limit)
                rows.append((subcommand, help_text))

            if rows:
                with formatter.section('Commands'):
                    formatter.write_dl(rows)


@click.group(cls=CustomGroup)
@click.version_option(version=__version__, prog_name='PDF Toolkit Pro')
@click.pass_context
def cli(ctx):
    """
    🚀 PDF Toolkit Pro - Herramienta profesional para PDFs
    
    Creada por Aroom Diaz Neyra - Automatiza operaciones con archivos PDF
    de forma rápida y eficiente desde la línea de comandos.
    
    Examples:
    
      Merge PDFs:
      $ pdf-toolkit merge file1.pdf file2.pdf -o combined.pdf
      
      Split PDF every 10 pages:
      $ pdf-toolkit split document.pdf --pages 10
      
      Extract specific pages:
      $ pdf-toolkit extract doc.pdf --pages 1,5,10-15 -o selection.pdf
    """
    ctx.ensure_object(dict)


# ============================================================================
# MERGE COMMANDS
# ============================================================================

@cli.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True), required=True)
@click.option(
    '-o', '--output',
    required=True,
    type=click.Path(),
    help='Output PDF file path'
)
@click.option(
    '--overwrite',
    is_flag=True,
    help='Overwrite output file if it exists'
)
@click.option(
    '--bookmarks',
    is_flag=True,
    help='Add bookmarks for each input file'
)
@click.option(
    '--no-progress',
    is_flag=True,
    help='Disable progress bar'
)
def merge(input_files, output, overwrite, bookmarks, no_progress):
    """
    Merge multiple PDF files into one.
    
    Examples:
    
      Merge two files:
      $ pdf-toolkit merge doc1.pdf doc2.pdf -o combined.pdf
      
      Merge with bookmarks:
      $ pdf-toolkit merge *.pdf -o all.pdf --bookmarks
      
      Merge all PDFs in directory:
      $ pdf-toolkit merge folder/*.pdf -o result.pdf
    """
    try:
        if bookmarks:
            merge_with_bookmarks(
                list(input_files),
                output,
                overwrite=overwrite
            )
        else:
            merge_pdfs(
                list(input_files),
                output,
                overwrite=overwrite,
                show_progress=not no_progress
            )
    except Exception as e:
        print_error(f"Merge failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option(
    '-o', '--output',
    required=True,
    type=click.Path(),
    help='Output PDF file path'
)
@click.option(
    '-r', '--recursive',
    is_flag=True,
    help='Search subdirectories recursively'
)
@click.option(
    '--overwrite',
    is_flag=True,
    help='Overwrite output file if it exists'
)
def merge_dir(directory, output, recursive, overwrite):
    """
    Merge all PDF files in a directory.
    
    Examples:
    
      Merge all PDFs in folder:
      $ pdf-toolkit merge-dir /path/to/pdfs -o combined.pdf
      
      Merge including subdirectories:
      $ pdf-toolkit merge-dir /path/to/pdfs -o all.pdf --recursive
    """
    try:
        merge_directory(
            directory,
            output,
            recursive=recursive,
            overwrite=overwrite
        )
    except Exception as e:
        print_error(f"Merge directory failed: {e}")
        sys.exit(1)


# ============================================================================
# SPLIT COMMANDS
# ============================================================================

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '-p', '--pages',
    type=int,
    required=True,
    help='Number of pages per split file'
)
@click.option(
    '--pattern',
    default='{base}_part{num}.pdf',
    help='Output filename pattern (default: {base}_part{num}.pdf)'
)
@click.option(
    '--overwrite',
    is_flag=True,
    help='Overwrite output files if they exist'
)
def split(input_file, pages, pattern, overwrite):
    """
    Split PDF into multiple files.
    
    Examples:
    
      Split every 10 pages:
      $ pdf-toolkit split document.pdf --pages 10
      
      Custom output pattern:
      $ pdf-toolkit split doc.pdf -p 5 --pattern "section_{num}.pdf"
    """
    try:
        split_by_pages(
            input_file,
            pages,
            output_pattern=pattern,
            overwrite=overwrite
        )
    except Exception as e:
        print_error(f"Split failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--at',
    'split_points',
    multiple=True,
    type=int,
    required=True,
    help='Page numbers to split at (can be used multiple times)'
)
@click.option(
    '--pattern',
    default='{base}_part{num}.pdf',
    help='Output filename pattern'
)
@click.option(
    '--overwrite',
    is_flag=True,
    help='Overwrite output files if they exist'
)
def split_at(input_file, split_points, pattern, overwrite):
    """
    Split PDF at specific page numbers.
    
    Examples:
    
      Split at pages 10 and 20:
      $ pdf-toolkit split-at doc.pdf --at 10 --at 20
      
      Result: Creates 3 files (pages 1-9, 10-19, 20-end)
    """
    try:
        split_at_pages(
            input_file,
            list(split_points),
            output_pattern=pattern,
            overwrite=overwrite
        )
    except Exception as e:
        print_error(f"Split at pages failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--output-dir',
    type=click.Path(),
    help='Output directory for page files'
)
@click.option(
    '--pattern',
    default='{base}_page{num}.pdf',
    help='Output filename pattern'
)
@click.option(
    '--overwrite',
    is_flag=True,
    help='Overwrite output files if they exist'
)
def split_pages(input_file, output_dir, pattern, overwrite):
    """
    Split PDF into individual pages.
    
    Examples:
    
      Extract all pages:
      $ pdf-toolkit split-pages document.pdf
      
      Save to specific directory:
      $ pdf-toolkit split-pages doc.pdf --output-dir ./pages/
    """
    try:
        split_into_singles(
            input_file,
            output_dir=output_dir,
            output_pattern=pattern,
            overwrite=overwrite
        )
    except Exception as e:
        print_error(f"Split into pages failed: {e}")
        sys.exit(1)


# ============================================================================
# INFO/UTILITY COMMANDS
# ============================================================================

@cli.command()
@click.argument('pdf_file', type=click.Path(exists=True))
def info(pdf_file):
    """
    Display information about a PDF file.
    
    Shows: number of pages, file size, metadata, etc.
    """
    try:
        from pypdf import PdfReader
        from .utils import format_file_size
        
        path = Path(pdf_file)
        reader = PdfReader(str(path))
        
        # File info
        file_size = path.stat().st_size
        
        click.echo(f"\n📄 PDF Information: {path.name}\n")
        click.echo(f"  Path:       {path.absolute()}")
        click.echo(f"  Size:       {format_file_size(file_size)}")
        click.echo(f"  Pages:      {len(reader.pages)}")
        
        # Metadata
        if reader.metadata:
            click.echo(f"\n  Metadata:")
            if reader.metadata.title:
                click.echo(f"    Title:    {reader.metadata.title}")
            if reader.metadata.author:
                click.echo(f"    Author:   {reader.metadata.author}")
            if reader.metadata.subject:
                click.echo(f"    Subject:  {reader.metadata.subject}")
            if reader.metadata.creator:
                click.echo(f"    Creator:  {reader.metadata.creator}")
            if reader.metadata.producer:
                click.echo(f"    Producer: {reader.metadata.producer}")
        
        click.echo()
        
    except Exception as e:
        print_error(f"Failed to read PDF info: {e}")
        sys.exit(1)


@cli.command()
def version():
    """Display version information."""
    from . import __version__
    click.echo(f"PDF Toolkit Pro v{__version__}")
    click.echo("Professional PDF manipulation tool")
    click.echo("\nFor help: pdf-toolkit --help")

@cli.command()
@click.argument('pdf_file', type=click.Path(exists=True))
def count(pdf_file):
    """
    Count the number of pages in a PDF file.
    
    Quick way to check how many pages a PDF has.
    
    Example:
    
      $ pdf-toolkit count document.pdf
      document.pdf has 42 pages
    """
    try:
        from pypdf import PdfReader
        from pathlib import Path
        
        path = Path(pdf_file)
        reader = PdfReader(str(path))
        num_pages = len(reader.pages)
        
        click.echo(f"\n📄 {path.name} has {num_pages} page{'s' if num_pages != 1 else ''}\n")
        
    except Exception as e:
        print_error(f"Failed to count pages: {e}")
        sys.exit(1)
        
if __name__ == '__main__':
    cli()
