# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "black>=25.9.0",
#     "rich>=14.1.0",
#     "typer>=0.19.2",
# ]
# ///
"""
Script to format Python code within {{ }} blocks in markdown files using Black.
"""

import re
from pathlib import Path
from typing import Annotated

import black
import typer
from rich.console import Console

console = Console()


def extract_python_blocks(content: str) -> list[tuple[str, str, str]]:
    """
    Extract Python code blocks from {{ }} and return (before, code, after) tuples.
    """
    pattern = r"(\{\{\s*)(.*?)(\s*\}\})"
    matches = []

    for match in re.finditer(pattern, content, re.DOTALL):
        before = match.group(1)  # {{ with whitespace
        code = match.group(2)  # Python code
        after = match.group(3)  # whitespace and }}
        matches.append((before, code, after))

    return matches


def format_python_code(code: str) -> str:
    """
    Format Python code using Black.
    """
    try:
        # Format the code with Black
        formatted = black.format_str(
            code,
            mode=black.Mode(
                target_versions={black.TargetVersion.PY39}, line_length=100, is_pyi=False
            ),
        )
        # Remove the trailing newline that Black adds
        return formatted.rstrip("\n")
    except Exception as e:
        console.print(f"[yellow]Warning: Could not format code block: {e}[/]")
        return code


def format_markdown_file(file_path: Path) -> bool:
    """
    Format Python code blocks in a markdown file.
    Returns True if any changes were made.
    """
    content = file_path.read_text(encoding="utf-8")
    original_content = content

    # Extract all Python blocks
    python_blocks = extract_python_blocks(content)

    if not python_blocks:
        return False

    # Format each block and replace in content
    for before, code, after in python_blocks:
        formatted_code = format_python_code(code)
        if formatted_code != code:
            # Replace the old block with the formatted one
            old_block = f"{before}{code}{after}"
            new_block = f"{before}{formatted_code}{after}"
            content = content.replace(old_block, new_block, 1)

    # Write back if changed
    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        return True

    return False


app = typer.Typer(
    help="Format Python code within {{ }} blocks in markdown files using Black.",
    epilog="""
Examples:
  format_macro_code.py docs/f2l.md docs/oll.md    # Format specific files
  format_macro_code.py docs/*.md                  # Format all markdown files in docs/
  format_macro_code.py --check docs/*.md          # Check if files need formatting
  format_macro_code.py --quiet docs/*.md          # Suppress output except errors
    """,
)


@app.command()
def main(
    files: Annotated[
        list[Path],
        typer.Argument(
            help="Markdown files to process",
            metavar="FILE",
        ),
    ],
    check: Annotated[
        bool,
        typer.Option(
            "--check",
            help="Don't write back modified files, just return status "
            "(exit code 1 if files would be reformatted)",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            "-q",
            help="Suppress output except for errors and warnings",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Show detailed information about processing",
        ),
    ] = False,
) -> None:
    """Format Python code within {{ }} blocks in markdown files using Black."""
    files_changed = 0
    files_that_need_formatting = 0

    for file_path in files:
        if not file_path.exists():
            console.print(f"[red]Error: File {file_path} does not exist[/]")
            continue

        if not file_path.suffix == ".md":
            if not quiet:
                console.print(f"[yellow]Warning: Skipping non-markdown file {file_path}[/]")
            continue

        if not quiet:
            console.print(f"[blue]Processing {file_path}...[/]")

        if check:
            # Check mode: don't modify files, just check if they would be formatted
            content = file_path.read_text(encoding="utf-8")
            python_blocks = extract_python_blocks(content)

            needs_formatting = False
            for before, code, after in python_blocks:
                formatted_code = format_python_code(code)
                if formatted_code != code:
                    needs_formatting = True
                    break

            if needs_formatting:
                files_that_need_formatting += 1
                if not quiet:
                    console.print(f"[yellow]  ! Would reformat {file_path}[/]")
            else:
                if verbose:
                    console.print(f"[magenta]  - No changes needed in {file_path}[/]")
        else:
            # Normal mode: format files
            if format_markdown_file(file_path):
                console.print(f"[green]  ✓ Formatted Python code in {file_path}[/]")
                files_changed += 1
            else:
                if verbose:
                    console.print(f"[magenta]  - No changes needed in {file_path}[/]")

    # Summary and exit code
    if check:
        if files_that_need_formatting > 0:
            if not quiet:
                console.print(
                    f"\n[bold yellow]{files_that_need_formatting} file(s) would be reformatted[/]"
                )
            raise typer.Exit(1)  # Exit with error code for CI/CD
        else:
            if not quiet:
                console.print("\n[bold green]All files are properly formatted[/]")
    else:
        if files_changed > 0:
            if not quiet:
                console.print(f"\n[bold green]Formatted {files_changed} file(s)[/]")
        else:
            if not quiet:
                console.print("\n[bold magenta]No files needed formatting[/]")


if __name__ == "__main__":
    app()
