# WORK IN PROGRESS

# PBNJ - Power BI Documentation & Analysis Tool

Transform .pbix files into readable, AI-friendly documentation to enable better collaboration and natural language workflows.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 What is PBNJ?

PBNJ helps Power BI developers share, document, understand, and work with Power BI files through automated documentation generation and interactive visualization. It transforms opaque .pbix files into readable, searchable documentation that enables better onboarding, collaboration, and AI-assisted workflows.

## ✨ Key Features

### 🔧 CLI Tool
- **Fast Setup**: Initialize projects from .pbix files in seconds
- **Multiple Formats**: Export to Markdown, HTML, JSON, and PDF
- **Git Integration**: Auto-initialize repositories with meaningful commits
- **Web Interface**: Local server for interactive exploration

### 📊 Documentation Generation
- **Technical Docs**: Complete DAX formulas, Power Query code, relationships
- **Business Docs**: High-level summaries and business logic explanations
- **AI-Ready**: Structured markdown optimized for Claude and other LLMs
- **Interactive**: Web interface for browsing and searching documentation

### 🔍 Analysis & Visualization
- **Data Model Explorer**: Interactive visualization of table relationships
- **Power Query Breakdown**: Step-by-step M code documentation
- **DAX Dependencies**: Formula relationships and lineage tracking
- **Full-Text Search**: Find anything across your entire Power BI model

## 🚀 Quick Start

### Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install PBNJ
git clone https://github.com/johns/pbnj
cd pbnj
uv sync
```

### Basic Usage

```bash
# Initialize a project from a .pbix file
pbnj init my-report.pbix

# Start the interactive web interface
pbnj serve

# Generate documentation only
pbnj docs

# Export to different formats
pbnj export --format pdf
pbnj export --format html

# Check project status
pbnj status
```

### Example Workflow

```bash
# 1. Create project from Power BI file
pbnj init --git sales-dashboard.pbix

# 2. Explore in web interface
pbnj serve

# 3. Export for sharing
pbnj export --format pdf --output sales-dashboard-docs.pdf

# 4. Commit documentation updates
pbnj git --message "Updated documentation for Q4 changes"
```

## 📖 Documentation Structure

PBNJ generates comprehensive documentation organized into:

- **Summary**: High-level overview and business context
- **Tables**: Data model structure and relationships
- **Measures**: DAX formulas with explanations and dependencies
- **Power Query**: M code with step-by-step transformations
- **Relationships**: Visual and textual relationship documentation
- **Technical**: Raw metadata and technical specifications

## 🧪 Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/pbnj

# Code formatting
uv run black src/ tests/
uv run isort src/ tests/

# Type checking
uv run mypy src/
```

### Project Structure

```
pbnj/
├── src/pbnj/              # Main package
│   ├── cli/               # Command-line interface
│   ├── core/              # Core parsing and git logic
│   ├── docs/              # Documentation generation
│   ├── templates/         # Jinja2 templates
│   └── web/               # FastAPI web server
├── tests/                 # Test suite
│   ├── test_*.py          # Unit tests
│   └── AdventureWorks.pbix # Sample test file
├── docs/                  # Generated documentation
└── pyproject.toml         # Project configuration
```

### Running Tests

See [tests/README.md](tests/README.md) for detailed testing instructions.

## 🔧 CLI Reference

### Commands

| Command | Description | Options |
|---------|-------------|---------|
| `pbnj init <pbix-file>` | Initialize project from .pbix file | `--output-dir`, `--force`, `--git` |
| `pbnj docs` | Generate documentation | `--output-dir`, `--format` |
| `pbnj serve` | Start web interface | `--host`, `--port`, `--reload` |
| `pbnj export` | Export documentation | `--format`, `--output` |
| `pbnj git` | Git operations | `--message` |
| `pbnj status` | Show project status | - |

### Global Options

- `--verbose, -v`: Enable verbose output
- `--version`: Show version information
- `--help`: Show help message

## 🌐 Web Interface

The local web interface provides:

- **Dashboard**: Model overview and statistics
- **Interactive Explorer**: Browse tables, measures, and relationships
- **Search**: Full-text search across documentation
- **Export Tools**: Download documentation in various formats
- **Live Updates**: Real-time documentation regeneration

Access at `http://localhost:8000` after running `pbnj serve`.

## 🤝 Contributing

We welcome contributions! Please see our development workflow:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with tests
4. Run the test suite: `uv run pytest`
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Use Black for code formatting
- Write tests for new features
- Update documentation for API changes
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [pbixray](https://github.com/pbixray/pbixray) - Core Power BI parsing library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Click](https://click.palletsprojects.com/) - Command-line interface framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/johns/pbnj/issues)
- **Documentation**: [Project Wiki](https://github.com/johns/pbnj/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/johns/pbnj/discussions)

---

**PBNJ** - Making Power BI documentation as smooth as peanut butter and jelly! 🥜🍇
