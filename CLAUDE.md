# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PBNJ is a Python CLI tool and web application that transforms Power BI (.pbix) files into readable, searchable, AI-friendly documentation. It extracts metadata from .pbix files using the pbixray library and generates comprehensive documentation in multiple formats (Markdown, HTML, JSON).

## Key Commands

### Development Setup
```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies 
uv sync

# Install development dependencies
uv sync --dev
```

### CLI Usage
```bash
# Initialize project from .pbix file
uv run pbnj init myfile.pbix

# Start web interface
uv run pbnj serve

# Generate documentation
uv run pbnj docs

# Export to different formats
uv run pbnj export markdown
```

### Testing and Code Quality
```bash
# Run tests
uv run pytest
uv run pytest --cov=src/pbnj

# Code formatting and linting
uv run black src/ tests/
uv run isort src/ tests/
uv run flake8 src/ tests/
uv run mypy src/
```

## Architecture

### Core Components
- **CLI Interface** (`src/pbnj/cli/main.py`): Click-based command-line tool with commands for init, docs, serve, export, git, and status
- **Parser Engine** (`src/pbnj/core/parser.py`): Uses pbixray library to extract metadata from .pbix files including tables, measures, relationships, and Power Query code
- **Documentation Generator** (`src/pbnj/docs/generator.py`): Jinja2-based templating system that generates multiple documentation formats from extracted metadata
- **Web Server** (`src/pbnj/web/server.py`): FastAPI application providing REST API endpoints and serving React frontend
- **Templates** (`src/pbnj/templates/`): Jinja2 templates for different documentation types (business, technical, tables, measures, etc.)

### Key Data Flow
1. PBIX file is parsed using pbixray to extract metadata
2. Metadata is saved to `.pbnj/metadata.json`
3. Documentation generator uses templates to create various documentation files in `docs/` directory
4. Web interface provides API endpoints to access metadata and documentation
5. Git integration allows tracking documentation changes over time

### Project Structure
Generated projects follow this structure:
```
project-name/
├── README.md              # Project overview
├── docs/                  # Generated documentation
│   ├── tables.md         # Data table structures  
│   ├── measures.md       # DAX measures and calculations
│   ├── relationships.md  # Data model relationships
│   ├── power_query.md    # ETL and data transformation
│   ├── technical.md      # Developer-focused details
│   ├── business.md       # Business stakeholder overview
│   └── summary.md        # Executive summary
└── .pbnj/                # PBNJ metadata and cache
    └── metadata.json     # Extracted .pbix metadata
```

## Important Implementation Details

- **Error Handling**: Core parsing methods include try/catch blocks that return error dictionaries if extraction fails
- **Template Fallbacks**: DocumentationGenerator includes default template fallbacks if template files are missing
- **Power Query Parsing**: Basic M code parsing extracts queries and steps, but could be enhanced for more sophisticated analysis
- **Web API State**: FastAPI server maintains global state for current project metadata
- **File Management**: Uses pathlib.Path throughout for cross-platform compatibility

## Dependencies

- **pbixray**: Core .pbix parsing library
- **click**: CLI framework
- **fastapi + uvicorn**: Web framework and server
- **jinja2**: Template engine for documentation generation
- **rich**: Enhanced CLI output formatting
- **gitpython**: Git integration capabilities

## Development Notes

- Code uses type hints throughout with mypy configuration for strict type checking
- Black and isort configured for consistent code formatting
- Pytest with coverage reporting for testing
- UV package manager for fast dependency resolution and virtual environment management
- Project follows Python package structure with hatchling build backend