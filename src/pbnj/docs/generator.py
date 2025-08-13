"""Documentation generation module for PBNJ."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, Template


class DocumentationGenerator:
    """Generate documentation from PBIX metadata."""
    
    def __init__(self, metadata: Dict[str, Any], output_dir: Path) -> None:
        """Initialize documentation generator."""
        self.metadata = metadata
        self.output_dir = output_dir
        self.docs_dir = output_dir / "docs"
        self.pbnj_dir = output_dir / ".pbnj"
        
        # Set up Jinja2 environment
        templates_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )
    
    @classmethod
    def from_metadata_file(cls, metadata_file: Path, output_dir: Path) -> "DocumentationGenerator":
        """Create generator from existing metadata file."""
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        return cls(metadata, output_dir)
    
    def generate_all(self) -> None:
        """Generate all documentation formats."""
        # Create directories
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.pbnj_dir.mkdir(parents=True, exist_ok=True)
        
        # Save metadata
        self._save_metadata()
        
        # Generate documentation
        self.generate_markdown()
        self._generate_summary()
        self._generate_technical_docs()
        self._generate_business_docs()
    
    def _save_metadata(self) -> None:
        """Save metadata to .pbnj directory."""
        metadata_file = self.pbnj_dir / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False, default=str)
    
    def generate_markdown(self) -> None:
        """Generate markdown documentation."""
        # Main README
        self._generate_readme()
        
        # Individual component docs
        self._generate_tables_doc()
        self._generate_measures_doc()
        self._generate_power_query_doc()
        self._generate_relationships_doc()
    
    def _generate_readme(self) -> None:
        """Generate main README.md file."""
        template = self._get_template("readme.md.j2")
        
        summary = {
            "file_name": self.metadata["file_info"]["name"],
            "file_size_mb": round(self.metadata["file_info"]["size_bytes"] / (1024 * 1024), 2),
            "table_count": len(self.metadata.get("tables", [])),
            "measure_count": len(self.metadata.get("measures", [])),
            "relationship_count": len(self.metadata.get("relationships", [])),
            "power_query_count": len(self.metadata.get("power_query", {}).get("queries", [])),
        }
        
        content = template.render(
            metadata=self.metadata,
            summary=summary,
        )
        
        readme_path = self.output_dir / "README.md"
        readme_path.write_text(content, encoding="utf-8")
    
    def _generate_tables_doc(self) -> None:
        """Generate tables documentation."""
        template = self._get_template("tables.md.j2")
        
        content = template.render(
            tables=self.metadata.get("tables", []),
        )
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        tables_path = self.docs_dir / "tables.md"
        tables_path.write_text(content, encoding="utf-8")
    
    def _generate_measures_doc(self) -> None:
        """Generate measures documentation."""
        template = self._get_template("measures.md.j2")
        
        # Clean up measures data to handle None values
        measures = self.metadata.get("measures", [])
        clean_measures = []
        for measure in measures:
            if isinstance(measure, dict):
                clean_measure = {
                    "name": measure.get("name") or "Unknown",
                    "table": measure.get("table") or "Unknown",
                    "description": measure.get("description") or "",
                    "expression": measure.get("expression") or "",
                    "display_folder": measure.get("display_folder") or "",
                    "format_string": measure.get("format_string") or "",
                    "data_type": measure.get("data_type") or "Unknown",
                }
                clean_measures.append(clean_measure)
        
        content = template.render(
            measures=clean_measures,
        )
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        measures_path = self.docs_dir / "measures.md"
        measures_path.write_text(content, encoding="utf-8")
    
    def _generate_power_query_doc(self) -> None:
        """Generate Power Query documentation."""
        template = self._get_template("power_query.md.j2")
        
        content = template.render(
            power_query=self.metadata.get("power_query", {}),
        )
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        pq_path = self.docs_dir / "power_query.md"
        pq_path.write_text(content, encoding="utf-8")
    
    def _generate_relationships_doc(self) -> None:
        """Generate relationships documentation."""
        template = self._get_template("relationships.md.j2")
        
        content = template.render(
            relationships=self.metadata.get("relationships", []),
        )
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        rel_path = self.docs_dir / "relationships.md"
        rel_path.write_text(content, encoding="utf-8")
    
    def _generate_summary(self) -> None:
        """Generate executive summary."""
        template = self._get_template("summary.md.j2")
        
        # Extract key insights
        insights = self._extract_insights()
        
        content = template.render(
            metadata=self.metadata,
            insights=insights,
        )
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        summary_path = self.docs_dir / "summary.md"
        summary_path.write_text(content, encoding="utf-8")
    
    def _generate_technical_docs(self) -> None:
        """Generate technical documentation for developers."""
        template = self._get_template("technical.md.j2")
        
        content = template.render(
            metadata=self.metadata,
        )
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        tech_path = self.docs_dir / "technical.md"
        tech_path.write_text(content, encoding="utf-8")
    
    def _generate_business_docs(self) -> None:
        """Generate business-friendly documentation."""
        template = self._get_template("business.md.j2")
        
        # Simplify technical details for business users
        business_data = self._simplify_for_business()
        
        content = template.render(
            metadata=self.metadata,
            business_data=business_data,
        )
        
        # Ensure docs directory exists
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        business_path = self.docs_dir / "business.md"
        business_path.write_text(content, encoding="utf-8")
    
    def generate_html(self) -> None:
        """Generate HTML documentation."""
        # Convert markdown to HTML
        # This is a placeholder - would use markdown library
        pass
    
    def generate_json(self) -> None:
        """Generate JSON documentation."""
        json_path = self.docs_dir / "metadata.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False, default=str)
    
    def export(self, format: str, output_path: Path) -> None:
        """Export documentation to specified format."""
        if format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False, default=str)
        elif format == "markdown":
            # Combine all markdown files
            combined_content = self._combine_markdown_files()
            output_path.write_text(combined_content, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _get_template(self, template_name: str) -> Template:
        """Get Jinja2 template, falling back to default if not found."""
        try:
            return self.jinja_env.get_template(template_name)
        except Exception:
            # Return a basic template if file doesn't exist
            return Template(self._get_default_template(template_name))
    
    def _get_default_template(self, template_name: str) -> str:
        """Get default template content."""
        if template_name == "readme.md.j2":
            return """# {{ metadata.file_info.name }}

## Summary
- **File**: {{ summary.file_name }}
- **Size**: {{ summary.file_size_mb }} MB
- **Tables**: {{ summary.table_count }}
- **Measures**: {{ summary.measure_count }}
- **Relationships**: {{ summary.relationship_count }}
- **Power Query Queries**: {{ summary.power_query_count }}

## Documentation
- [Tables](docs/tables.md)
- [Measures](docs/measures.md)
- [Power Query](docs/power_query.md)
- [Relationships](docs/relationships.md)
- [Technical Details](docs/technical.md)
- [Business Overview](docs/business.md)
"""
        elif template_name == "tables.md.j2":
            return """# Tables

{% for table in tables %}
## {{ table.name }}
{% if table.description %}
**Description**: {{ table.description }}
{% endif %}
**Type**: {{ table.type }}
**Hidden**: {{ table.hidden }}

{% endfor %}
"""
        else:
            return f"# {template_name}\n\nTemplate not found. Please create the template file."
    
    def _extract_insights(self) -> Dict[str, Any]:
        """Extract key insights from metadata."""
        insights = {
            "complexity_score": self._calculate_complexity_score(),
            "data_sources": self._identify_data_sources(),
            "key_metrics": self._identify_key_metrics(),
        }
        return insights
    
    def _calculate_complexity_score(self) -> int:
        """Calculate a complexity score based on various factors."""
        score = 0
        score += len(self.metadata.get("tables", [])) * 2
        score += len(self.metadata.get("measures", [])) * 3
        score += len(self.metadata.get("relationships", [])) * 1
        score += len(self.metadata.get("power_query", {}).get("queries", [])) * 2
        return score
    
    def _identify_data_sources(self) -> List[str]:
        """Identify data sources from Power Query."""
        sources = []
        # Extract from Power Query code
        pq = self.metadata.get("power_query", {})
        if "raw_code" in pq:
            # Simple extraction - could be more sophisticated
            if "Excel" in str(pq["raw_code"]):
                sources.append("Excel")
            if "SQL" in str(pq["raw_code"]):
                sources.append("SQL Server")
            if "SharePoint" in str(pq["raw_code"]):
                sources.append("SharePoint")
        return sources
    
    def _identify_key_metrics(self) -> List[str]:
        """Identify key business metrics."""
        metrics = []
        measures = self.metadata.get("measures", [])
        for measure in measures[:5]:  # Top 5 measures
            if isinstance(measure, dict) and "name" in measure:
                metrics.append(measure["name"])
        return metrics
    
    def _simplify_for_business(self) -> Dict[str, Any]:
        """Simplify technical data for business users."""
        return {
            "overview": f"This Power BI file contains {len(self.metadata.get('tables', []))} data tables with {len(self.metadata.get('measures', []))} calculated metrics.",
            "key_insights": self._extract_insights(),
            "data_sources": self._identify_data_sources(),
        }
    
    def _combine_markdown_files(self) -> str:
        """Combine all markdown files into one."""
        combined = []
        
        # Add README content
        readme_path = self.output_dir / "README.md"
        if readme_path.exists():
            combined.append(readme_path.read_text(encoding="utf-8"))
        
        # Add all docs
        for doc_file in self.docs_dir.glob("*.md"):
            combined.append(f"\n\n---\n\n")
            combined.append(doc_file.read_text(encoding="utf-8"))
        
        return "\n".join(combined)