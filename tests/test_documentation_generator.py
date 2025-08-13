"""Tests for documentation generator functionality."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pbnj.docs.generator import DocumentationGenerator


class TestDocumentationGenerator:
    """Test cases for DocumentationGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_metadata = {
            "file_info": {
                "name": "test.pbix",
                "path": "/path/to/test.pbix",
                "size_bytes": 1000000
            },
            "tables": [
                {
                    "name": "DimCustomer",
                    "type": "Table",
                    "description": "Customer dimension table",
                    "hidden": False,
                    "columns": []
                },
                {
                    "name": "FactSales",
                    "type": "Table", 
                    "description": "Sales fact table",
                    "hidden": False,
                    "columns": []
                }
            ],
            "measures": [
                {
                    "name": "Total Sales",
                    "formula": "SUM(FactSales[Amount])",
                    "table": "FactSales"
                },
                {
                    "name": "Customer Count", 
                    "formula": "DISTINCTCOUNT(DimCustomer[CustomerID])",
                    "table": "DimCustomer"
                }
            ],
            "relationships": [
                {
                    "from_table": "FactSales",
                    "to_table": "DimCustomer",
                    "from_column": "CustomerID",
                    "to_column": "CustomerID"
                }
            ],
            "power_query": {
                "queries": [
                    {
                        "name": "DimCustomer",
                        "code": "let Source = Excel.Workbook(...) in Source",
                        "steps": ["Source = Excel.Workbook(...)", "Result = Source"]
                    }
                ],
                "raw_code": "let Source = Excel.Workbook(...) in Source"
            },
            "parameters": [],
            "metadata": {}
        }
        
    def test_generator_initialization(self):
        """Test generator initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            
            assert generator.metadata == self.sample_metadata
            assert generator.output_dir == temp_path
            assert generator.docs_dir == temp_path / "docs"
            assert generator.pbnj_dir == temp_path / ".pbnj"
            assert generator.jinja_env is not None
            
    def test_from_metadata_file(self):
        """Test creating generator from metadata file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            metadata_file = temp_path / "metadata.json"
            
            # Create metadata file
            with open(metadata_file, 'w') as f:
                json.dump(self.sample_metadata, f)
                
            generator = DocumentationGenerator.from_metadata_file(metadata_file, temp_path)
            
            assert generator.metadata == self.sample_metadata
            assert generator.output_dir == temp_path
            
    def test_generate_all(self):
        """Test generating all documentation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.generate_all()
            
            # Check directories were created
            assert generator.docs_dir.exists()
            assert generator.pbnj_dir.exists()
            
            # Check metadata was saved
            metadata_file = generator.pbnj_dir / "metadata.json"
            assert metadata_file.exists()
            
            with open(metadata_file, 'r') as f:
                saved_metadata = json.load(f)
            assert saved_metadata == self.sample_metadata
            
            # Check documentation files were created
            assert (temp_path / "README.md").exists()
            assert (generator.docs_dir / "tables.md").exists()
            assert (generator.docs_dir / "measures.md").exists()
            assert (generator.docs_dir / "power_query.md").exists()
            assert (generator.docs_dir / "relationships.md").exists()
            
    def test_generate_readme(self):
        """Test README generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator._generate_readme()
            
            readme_file = temp_path / "README.md"
            assert readme_file.exists()
            
            content = readme_file.read_text()
            assert "test.pbix" in content
            content_lower = content.lower()
            assert "tables**: 2" in content_lower or "table_count" in content_lower
            assert "measures**: 2" in content_lower or "measure_count" in content_lower
            
    def test_generate_tables_doc(self):
        """Test tables documentation generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.docs_dir.mkdir(parents=True, exist_ok=True)
            generator._generate_tables_doc()
            
            tables_file = generator.docs_dir / "tables.md"
            assert tables_file.exists()
            
            content = tables_file.read_text()
            assert "DimCustomer" in content
            assert "FactSales" in content
            assert "Customer dimension table" in content
            
    def test_generate_measures_doc(self):
        """Test measures documentation generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.docs_dir.mkdir(parents=True, exist_ok=True)
            generator._generate_measures_doc()
            
            measures_file = generator.docs_dir / "measures.md"
            assert measures_file.exists()
            
            content = measures_file.read_text()
            assert "Total Sales" in content or "measures" in content.lower()
            
    def test_generate_power_query_doc(self):
        """Test Power Query documentation generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.docs_dir.mkdir(parents=True, exist_ok=True)
            generator._generate_power_query_doc()
            
            pq_file = generator.docs_dir / "power_query.md"
            assert pq_file.exists()
            
            content = pq_file.read_text()
            # Should contain Power Query content or template
            assert len(content) > 0
            
    def test_generate_relationships_doc(self):
        """Test relationships documentation generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.docs_dir.mkdir(parents=True, exist_ok=True)
            generator._generate_relationships_doc()
            
            rel_file = generator.docs_dir / "relationships.md"
            assert rel_file.exists()
            
            content = rel_file.read_text()
            # Should contain relationships content or template
            assert len(content) > 0
            
    def test_generate_markdown(self):
        """Test markdown generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.generate_markdown()
            
            # Check that README and docs were created
            assert (temp_path / "README.md").exists()
            assert (generator.docs_dir / "tables.md").exists()
            assert (generator.docs_dir / "measures.md").exists()
            
    def test_generate_json(self):
        """Test JSON generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.docs_dir.mkdir(parents=True, exist_ok=True)
            generator.generate_json()
            
            json_file = generator.docs_dir / "metadata.json"
            assert json_file.exists()
            
            with open(json_file, 'r') as f:
                saved_data = json.load(f)
            assert saved_data == self.sample_metadata
            
    def test_export_json(self):
        """Test JSON export."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_file = temp_path / "export.json"
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.export("json", output_file)
            
            assert output_file.exists()
            with open(output_file, 'r') as f:
                exported_data = json.load(f)
            assert exported_data == self.sample_metadata
            
    def test_export_markdown(self):
        """Test markdown export."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_file = temp_path / "export.md"
            
            # Create some documentation files first
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            generator.generate_markdown()
            
            generator.export("markdown", output_file)
            
            assert output_file.exists()
            content = output_file.read_text()
            assert len(content) > 0
            
    def test_export_unsupported_format(self):
        """Test export with unsupported format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            output_file = temp_path / "export.xyz"
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            
            with pytest.raises(ValueError, match="Unsupported export format"):
                generator.export("xyz", output_file)
                
    def test_get_template_fallback(self):
        """Test template fallback mechanism."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            
            # Test with non-existent template
            template = generator._get_template("nonexistent.j2")
            assert template is not None
            
            # Test with known template names
            readme_template = generator._get_template("readme.md.j2")
            assert readme_template is not None
            
            tables_template = generator._get_template("tables.md.j2")
            assert tables_template is not None
            
    def test_extract_insights(self):
        """Test insights extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            insights = generator._extract_insights()
            
            assert "complexity_score" in insights
            assert "data_sources" in insights
            assert "key_metrics" in insights
            assert insights["complexity_score"] > 0
            
    def test_calculate_complexity_score(self):
        """Test complexity score calculation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            score = generator._calculate_complexity_score()
            
            # Should be > 0 based on our sample data
            # 2 tables * 2 + 2 measures * 3 + 1 relationship * 1 + 1 query * 2 = 13
            expected_score = 2*2 + 2*3 + 1*1 + 1*2
            assert score == expected_score
            
    def test_identify_data_sources(self):
        """Test data source identification."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test with Excel source
            metadata_with_excel = self.sample_metadata.copy()
            metadata_with_excel["power_query"]["raw_code"] = "Excel.Workbook(File.Contents('data.xlsx'))"
            
            generator = DocumentationGenerator(metadata_with_excel, temp_path)
            sources = generator._identify_data_sources()
            
            assert "Excel" in sources
            
    def test_identify_key_metrics(self):
        """Test key metrics identification."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            metrics = generator._identify_key_metrics()
            
            assert "Total Sales" in metrics
            assert "Customer Count" in metrics
            
    def test_simplify_for_business(self):
        """Test business data simplification."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            business_data = generator._simplify_for_business()
            
            assert "overview" in business_data
            assert "key_insights" in business_data
            assert "data_sources" in business_data
            assert "2 data tables" in business_data["overview"]
            assert "2 calculated metrics" in business_data["overview"]
            
    def test_combine_markdown_files(self):
        """Test combining markdown files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            
            # Create some documentation files
            generator.generate_markdown()
            
            combined = generator._combine_markdown_files()
            
            assert len(combined) > 0
            # Should contain content from multiple files
            assert "test.pbix" in combined  # From README
            
    def test_generate_with_empty_metadata(self):
        """Test generation with empty metadata."""
        empty_metadata = {
            "file_info": {"name": "empty.pbix", "path": "/empty.pbix", "size_bytes": 100},
            "tables": [],
            "measures": [],
            "relationships": [],
            "power_query": {"queries": []},
            "parameters": [],
            "metadata": {}
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(empty_metadata, temp_path)
            generator.generate_all()
            
            # Should still create files even with empty data
            assert (temp_path / "README.md").exists()
            assert (generator.docs_dir / "tables.md").exists()
            
    def test_generate_with_missing_template_files(self):
        """Test generation when template files are missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create generator with non-existent templates directory
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            
            # Mock the jinja environment to simulate missing template files
            with patch.object(generator.jinja_env, 'get_template') as mock_get_template:
                mock_get_template.side_effect = Exception("Template not found")
                
                # Should use fallback templates
                generator.generate_markdown()
                
                # Files should still be created
                assert (temp_path / "README.md").exists()
                assert (generator.docs_dir / "tables.md").exists()


class TestDocumentationGeneratorEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_metadata = {
            "file_info": {
                "name": "test.pbix",
                "path": "/path/to/test.pbix",
                "size_bytes": 1000000
            },
            "tables": [],
            "measures": [],
            "relationships": [],
            "power_query": {"queries": []},
            "parameters": [],
            "metadata": {}
        }
    
    def test_generate_with_malformed_metadata(self):
        """Test generation with malformed metadata."""
        malformed_metadata = {
            "file_info": None,  # Should be dict
            "tables": "not_a_list",  # Should be list
            "measures": [{"name": "test"}],  # Missing required fields
            "relationships": [{}],  # Empty relationship
            "power_query": None  # Should be dict
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(malformed_metadata, temp_path)
            
            # Should handle gracefully without crashing
            try:
                generator.generate_all()
                # If it succeeds, that's good
                assert True
            except Exception as e:
                # If it fails, the error should be handled gracefully
                assert "file_info" in str(e) or "metadata" in str(e)
                
    def test_generate_with_permission_error(self):
        """Test generation with permission errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(self.sample_metadata, temp_path)
            
            # Mock file writing to raise permission error
            with patch('pathlib.Path.write_text') as mock_write:
                mock_write.side_effect = PermissionError("Access denied")
                
                with pytest.raises(PermissionError):
                    generator._generate_readme()
                    
    def test_generate_with_unicode_content(self):
        """Test generation with unicode content in metadata."""
        unicode_metadata = {
            "file_info": {
                "name": "тест.pbix",  # Cyrillic
                "path": "/path/to/тест.pbix",
                "size_bytes": 1000000
            },
            "tables": [
                {
                    "name": "Müßter",  # German umlaut
                    "description": "Ťабле with ůnicode çhars 中文",  # Mixed unicode
                    "type": "Table",
                    "hidden": False
                }
            ],
            "measures": [],
            "relationships": [],
            "power_query": {"queries": []},
            "parameters": [],
            "metadata": {}
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            generator = DocumentationGenerator(unicode_metadata, temp_path)
            generator.generate_all()
            
            # Should handle unicode correctly
            readme_file = temp_path / "README.md"
            assert readme_file.exists()
            
            content = readme_file.read_text(encoding='utf-8')
            assert "тест.pbix" in content


# Sample metadata for testing
sample_metadata = {
    "file_info": {
        "name": "test.pbix",
        "path": "/path/to/test.pbix", 
        "size_bytes": 1000000
    },
    "tables": [],
    "measures": [],
    "relationships": [],
    "power_query": {"queries": []},
    "parameters": [],
    "metadata": {}
}


if __name__ == "__main__":
    pytest.main([__file__])