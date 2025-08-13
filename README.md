# 🥜 PBNJ - Power BI Documentation & Analysis Tool

> **PB**eanut **B**utter & **J**elly for Power BI - Making .pbix files digestible for everyone

Transform opaque Power BI files into readable, searchable, AI-friendly documentation that enables better onboarding, collaboration, and natural language workflows.

## ✨ Features

- **📊 Complete .pbix Analysis**: Extract tables, measures, relationships, and Power Query code
- **📚 Multi-Format Documentation**: Generate markdown, HTML, and JSON documentation
- **🤖 AI-Ready Output**: Optimized for Claude projects and LLM workflows
- **🌐 Interactive Web UI**: Local web interface for exploring your data model
- **👥 Multi-Audience**: Technical docs for developers, business overviews for stakeholders
- **🔧 CLI & Web**: Command-line tool with optional web interface
- **📝 Git Integration**: Initialize repos and track documentation changes

## 🚀 Quick Start

### Installation

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup PBNJ
git clone https://github.com/johns/pbnj.git
cd pbnj
uv sync
```

### Basic Usage

```bash
# Initialize project from .pbix file
uv run pbnj init myfile.pbix

# Start interactive web interface
uv run pbnj serve

# Generate documentation
uv run pbnj docs

# Export to different formats
uv run pbnj export markdown
```

## 🎯 Use Cases

### For Power BI Developers
- **Onboarding**: Quickly understand complex .pbix files
- **Documentation**: Generate comprehensive technical documentation
- **Code Review**: Review DAX measures and Power Query transformations
- **Migration**: Document existing models before major changes

### For Business Stakeholders
- **Understanding**: Get business-friendly explanations of data models
- **Governance**: Track data sources, metrics, and business logic
- **Communication**: Share model insights with non-technical team members

### For AI-Assisted Workflows
- **Claude Projects**: Import structured documentation for natural language queries
- **DAX Generation**: Use existing patterns to generate new measures
- **Model Analysis**: Ask AI to explain relationships and business logic
- **Change Requests**: Describe desired changes in natural language

## 📁 Project Structure

```
your-project/
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

## 🛠️ CLI Commands

### Core Commands
```bash
pbnj init <pbix-file>      # Initialize project from .pbix file
pbnj docs generate         # Generate/regenerate documentation
pbnj serve                 # Start local web interface
pbnj status               # Show project status
```

### Export & Integration
```bash
pbnj export json          # Export metadata as JSON
pbnj export markdown      # Export combined markdown
pbnj git setup           # Initialize git repo with documentation
```

### Web Interface Options
```bash
pbnj serve --host 0.0.0.0 --port 8080  # Custom host/port
pbnj serve --reload                     # Development mode with auto-reload
```

## 🌐 Web Interface

The local web interface provides:

- **📊 Interactive Dashboard**: Visual overview of your data model
- **🔍 Searchable Documentation**: Full-text search across all extracted metadata
- **📈 Relationship Visualizer**: Interactive data model diagrams
- **📝 Live Documentation**: Browse generated docs with real-time updates
- **💾 Export Tools**: Download documentation in various formats

Access at `http://localhost:8000` after running `pbnj serve`

## 🤖 AI Integration Examples

### With Claude Projects

1. **Initialize Documentation**:
   ```bash
   pbnj init sales_dashboard.pbix
   pbnj export markdown -o claude_context.md
   ```

2. **Add to Claude Project**: Upload `claude_context.md` to your Claude project

3. **Natural Language Queries**:
   ```
   "Create a new DAX measure for year-over-year growth based on the existing sales measures"
   "Explain the relationship between Customer and Sales tables in business terms"
   "What data transformations are applied in the Power Query for the Product table?"
   ```

### Example Workflows

#### New Team Member Onboarding
```bash
# Generate comprehensive documentation
pbnj init complex_model.pbix --git
pbnj docs generate

# Share repository with new team member
git remote add origin <repo-url>
git push -u origin main
```

#### Pre-Migration Documentation
```bash
# Document current state before changes
pbnj init legacy_model.pbix
pbnj git setup
git commit -m "Document legacy model before migration"

# After migration, compare changes
pbnj init new_model.pbix
git add . && git commit -m "Document new model post-migration"
```

## 🏗️ Architecture

### Core Components
- **Parser Engine**: Uses [pbixray](https://github.com/Hugoberry/pbixray) for .pbix metadata extraction
- **Documentation Generator**: Jinja2-based templating system
- **Web Server**: FastAPI with REST endpoints
- **CLI Interface**: Click-based command-line tool

### Technology Stack
- **Backend**: Python 3.11+ with UV package management
- **Web Framework**: FastAPI + Uvicorn
- **Frontend**: React (planned for Phase 2)
- **Parsing**: pbixray library
- **Documentation**: Jinja2 templates + Markdown
- **Git Integration**: GitPython

## 🔧 Development

### Setup Development Environment
```bash
git clone https://github.com/johns/pbnj.git
cd pbnj
uv sync --dev
```

### Run Tests
```bash
uv run pytest
uv run pytest --cov=src/pbnj
```

### Code Quality
```bash
uv run black src/ tests/
uv run isort src/ tests/
uv run flake8 src/ tests/
uv run mypy src/
```

## 📋 Roadmap

### Phase 1: Core CLI Tool ✅
- [x] PBIX parsing with pbixray
- [x] Markdown documentation generation
- [x] Basic CLI commands
- [x] Git integration

### Phase 2: Web Interface (In Progress)
- [x] FastAPI REST API
- [ ] React frontend
- [ ] Interactive visualizations
- [ ] Real-time documentation updates

### Phase 3: Advanced Features (Planned)
- [ ] Advanced relationship diagrams
- [ ] Data lineage visualization
- [ ] Performance analysis
- [ ] Team collaboration features
- [ ] VS Code extension

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Areas for Contribution
- **Parsing Improvements**: Enhance pbixray integration
- **Template Development**: Create new documentation templates
- **Web UI**: React frontend development
- **Testing**: Add comprehensive test coverage
- **Documentation**: Improve user guides and API docs

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [pbixray](https://github.com/Hugoberry/pbixray) - Core .pbix parsing capabilities
- [UV](https://github.com/astral-sh/uv) - Fast Python package management
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Click](https://click.palletsprojects.com/) - CLI framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/johns/pbnj/issues)
- **Discussions**: [GitHub Discussions](https://github.com/johns/pbnj/discussions)
- **Documentation**: [Wiki](https://github.com/johns/pbnj/wiki)

---

*PBNJ - Making Power BI files as easy to understand as peanut butter & jelly* 🥜