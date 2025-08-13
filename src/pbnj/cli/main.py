"""PBNJ CLI main entry point."""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from pbnj import __version__
from pbnj.core.parser import PBIXParser
from pbnj.docs.generator import DocumentationGenerator
from pbnj.web.server import start_server

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="pbnj")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def cli(verbose: bool) -> None:
    """PBNJ - Power BI Documentation & Analysis Tool.
    
    Transform .pbix files into readable, AI-friendly documentation.
    """
    if verbose:
        console.print(f"[dim]PBNJ v{__version__} - Verbose mode enabled[/dim]")


@cli.command()
@click.argument("pbix_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), help="Output directory for project")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files")
@click.option("--git", is_flag=True, help="Initialize git repository")
def init(pbix_file: Path, output_dir: Optional[Path], force: bool, git: bool) -> None:
    """Initialize a new PBNJ project from a .pbix file."""
    try:
        if output_dir is None:
            output_dir = Path.cwd() / pbix_file.stem
        
        console.print(f"[blue]Initializing PBNJ project from[/blue] {pbix_file}")
        console.print(f"[blue]Output directory:[/blue] {output_dir}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=force)
        
        # Parse the PBIX file
        with console.status("[bold green]Parsing PBIX file..."):
            parser = PBIXParser(pbix_file)
            metadata = parser.extract_metadata()
        
        console.print("[green]✓[/green] PBIX file parsed successfully")
        
        # Generate documentation
        with console.status("[bold green]Generating documentation..."):
            doc_gen = DocumentationGenerator(metadata, output_dir)
            doc_gen.generate_all()
        
        console.print("[green]✓[/green] Documentation generated")
        
        # Initialize git if requested
        if git:
            from pbnj.core.git_integration import GitHelper
            git_helper = GitHelper(output_dir)
            git_helper.init_repo()
            console.print("[green]✓[/green] Git repository initialized")
        
        console.print(f"\n[bold green]Project initialized successfully![/bold green]")
        console.print(f"[dim]Run 'pbnj serve' in {output_dir} to start the web interface[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), help="Output directory")
@click.option("--format", "-f", type=click.Choice(["markdown", "html", "json"]), default="markdown", help="Output format")
def docs(output_dir: Optional[Path], format: str) -> None:
    """Generate documentation from existing project."""
    try:
        if output_dir is None:
            output_dir = Path.cwd()
        
        console.print(f"[blue]Generating documentation in[/blue] {output_dir}")
        
        # Look for existing metadata
        metadata_file = output_dir / ".pbnj" / "metadata.json"
        if not metadata_file.exists():
            console.print("[red]Error:[/red] No PBNJ project found. Run 'pbnj init' first.")
            sys.exit(1)
        
        with console.status("[bold green]Generating documentation..."):
            doc_gen = DocumentationGenerator.from_metadata_file(metadata_file, output_dir)
            if format == "markdown":
                doc_gen.generate_markdown()
            elif format == "html":
                doc_gen.generate_html()
            elif format == "json":
                doc_gen.generate_json()
        
        console.print(f"[green]✓[/green] Documentation generated in {format} format")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
def serve(host: str, port: int, reload: bool) -> None:
    """Start the local web interface."""
    try:
        # Check for PBNJ project
        if not (Path.cwd() / ".pbnj").exists():
            console.print("[red]Error:[/red] No PBNJ project found. Run 'pbnj init' first.")
            sys.exit(1)
        
        console.print(f"[blue]Starting PBNJ web interface at[/blue] http://{host}:{port}")
        console.print("[dim]Press Ctrl+C to stop[/dim]")
        
        start_server(host=host, port=port, reload=reload)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped[/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--format", "-f", type=click.Choice(["pdf", "html", "json", "markdown"]), required=True, help="Export format")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
def export(format: str, output: Optional[Path]) -> None:
    """Export documentation to various formats."""
    try:
        # Check for PBNJ project
        metadata_file = Path.cwd() / ".pbnj" / "metadata.json"
        if not metadata_file.exists():
            console.print("[red]Error:[/red] No PBNJ project found. Run 'pbnj init' first.")
            sys.exit(1)
        
        if output is None:
            output = Path.cwd() / f"pbnj_export.{format}"
        
        console.print(f"[blue]Exporting to[/blue] {format} [blue]format:[/blue] {output}")
        
        with console.status(f"[bold green]Exporting to {format}..."):
            doc_gen = DocumentationGenerator.from_metadata_file(metadata_file, Path.cwd())
            doc_gen.export(format, output)
        
        console.print(f"[green]✓[/green] Exported to {output}")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--message", "-m", help="Commit message")
def git(message: Optional[str]) -> None:
    """Git integration commands."""
    try:
        from pbnj.core.git_integration import GitHelper
        
        git_helper = GitHelper()
        
        if not git_helper.is_git_repo():
            console.print("[yellow]Initializing git repository...[/yellow]")
            git_helper.init_repo()
        
        # Add and commit changes
        if message is None:
            message = "Update PBNJ documentation"
        
        with console.status("[bold green]Committing changes..."):
            git_helper.commit_changes(message)
        
        console.print("[green]✓[/green] Changes committed to git")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
def status() -> None:
    """Show project status."""
    try:
        cwd = Path.cwd()
        pbnj_dir = cwd / ".pbnj"
        
        table = Table(title="PBNJ Project Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="dim")
        
        # Check project initialization
        if pbnj_dir.exists():
            table.add_row("Project", "✓ Initialized", str(cwd))
            
            # Check metadata
            metadata_file = pbnj_dir / "metadata.json"
            if metadata_file.exists():
                table.add_row("Metadata", "✓ Available", f"Size: {metadata_file.stat().st_size} bytes")
            else:
                table.add_row("Metadata", "✗ Missing", "Run 'pbnj init' to generate")
            
            # Check documentation
            docs_dir = cwd / "docs"
            if docs_dir.exists():
                doc_count = len(list(docs_dir.glob("*.md")))
                table.add_row("Documentation", "✓ Generated", f"{doc_count} files")
            else:
                table.add_row("Documentation", "✗ Missing", "Run 'pbnj docs' to generate")
            
            # Check git
            git_dir = cwd / ".git"
            if git_dir.exists():
                table.add_row("Git", "✓ Initialized", "Repository ready")
            else:
                table.add_row("Git", "✗ Not initialized", "Run 'pbnj init --git' or 'pbnj git'")
                
        else:
            table.add_row("Project", "✗ Not initialized", "Run 'pbnj init <pbix-file>'")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()