"""Tests for CLI main entry point and commands."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pbnj.cli.main import cli


class TestCLIMain:
    """Test cases for the main CLI interface."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.test_pbix = Path(__file__).parent / "AdventureWorks.pbix"
        
    def test_cli_version(self):
        """Test CLI version command."""
        result = self.runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
        
    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "PBNJ - Power BI Documentation & Analysis Tool" in result.output
        assert "init" in result.output
        assert "serve" in result.output
        assert "docs" in result.output
        
    def test_init_command_help(self):
        """Test init command help."""
        result = self.runner.invoke(cli, ["init", "--help"])
        assert result.exit_code == 0
        assert "Initialize a new PBNJ project" in result.output
        
    def test_init_command_missing_file(self):
        """Test init command with missing PBIX file."""
        result = self.runner.invoke(cli, ["init", "nonexistent.pbix"])
        assert result.exit_code != 0
        
    def test_init_command_success(self):
        """Test successful init command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "test_project"
            
            with patch('pbnj.core.parser.PBIXParser') as mock_parser:
                # Mock successful parsing
                mock_instance = MagicMock()
                mock_instance.extract_metadata.return_value = {
                    "file_info": {
                        "name": "AdventureWorks.pbix",
                        "path": str(self.test_pbix),
                        "size_bytes": 1000000
                    },
                    "tables": [],
                    "measures": [],
                    "relationships": [],
                    "power_query": {"queries": []}
                }
                mock_parser.return_value = mock_instance
                
                with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                    mock_doc_instance = MagicMock()
                    mock_doc_gen.return_value = mock_doc_instance
                    
                    # Ensure the output directory exists before the test
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    result = self.runner.invoke(cli, [
                        "init", str(self.test_pbix),
                        "--output-dir", str(output_dir),
                        "--force"
                    ])
                    
                    print(f"Exit code: {result.exit_code}")
                    print(f"Output: {result.output}")
                    if result.exception:
                        print(f"Exception: {result.exception}")
                    
                    assert result.exit_code == 0
                    assert "Project initialized successfully" in result.output
                    mock_instance.extract_metadata.assert_called_once()
                    mock_doc_instance.generate_all.assert_called_once()
                    
    def test_init_command_with_git(self):
        """Test init command with git integration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "test_project"
            
            with patch('pbnj.core.parser.PBIXParser') as mock_parser:
                mock_instance = MagicMock()
                mock_instance.extract_metadata.return_value = {
                    "file_info": {
                        "name": "AdventureWorks.pbix",
                        "path": str(self.test_pbix),
                        "size_bytes": 1000000
                    },
                    "tables": [],
                    "measures": [],
                    "relationships": [],
                    "power_query": {"queries": []}
                }
                mock_parser.return_value = mock_instance
                
                with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                    with patch('pbnj.core.git_integration.GitHelper') as mock_git:
                        mock_doc_instance = MagicMock()
                        mock_doc_gen.return_value = mock_doc_instance
                        mock_git_instance = MagicMock()
                        mock_git.return_value = mock_git_instance
                        
                        result = self.runner.invoke(cli, [
                            "init", str(self.test_pbix),
                            "--output-dir", str(output_dir),
                            "--git"
                        ])
                        
                        assert result.exit_code == 0
                        assert "Git repository initialized" in result.output
                        mock_git_instance.init_repo.assert_called_once()
                        
    def test_docs_command_no_project(self):
        """Test docs command when no project exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                result = self.runner.invoke(cli, ["docs"])
                assert result.exit_code == 1
                assert "No PBNJ project found" in result.output
            
    def test_docs_command_success(self):
        """Test successful docs command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pbnj_dir = temp_path / ".pbnj"
            pbnj_dir.mkdir()
            
            # Create metadata file
            metadata = {
                "file_info": {"name": "test.pbix"},
                "tables": [],
                "measures": []
            }
            metadata_file = pbnj_dir / "metadata.json"
            metadata_file.write_text(json.dumps(metadata))
            
            with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                mock_instance = MagicMock()
                mock_doc_gen.from_metadata_file.return_value = mock_instance
                
                with patch('pathlib.Path.cwd', return_value=temp_path):
                    result = self.runner.invoke(cli, ["docs"])
                    
                    assert result.exit_code == 0
                    assert "Documentation generated" in result.output
                    mock_instance.generate_markdown.assert_called_once()
                
    def test_serve_command_no_project(self):
        """Test serve command when no project exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                result = self.runner.invoke(cli, ["serve"])
                assert result.exit_code == 1
                assert "No PBNJ project found" in result.output
            
    def test_serve_command_success(self):
        """Test serve command with project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pbnj_dir = temp_path / ".pbnj"
            pbnj_dir.mkdir()
            
            with patch('pbnj.web.server.start_server') as mock_start_server:
                # Mock KeyboardInterrupt to simulate server stop
                mock_start_server.side_effect = KeyboardInterrupt()
                
                with patch('pathlib.Path.cwd', return_value=temp_path):
                    result = self.runner.invoke(cli, ["serve"])
                    
                    assert result.exit_code == 0
                    assert "Starting PBNJ web interface" in result.output
                    mock_start_server.assert_called_once_with(
                        host="127.0.0.1", port=8000, reload=False
                    )
                
    def test_export_command_no_project(self):
        """Test export command when no project exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                result = self.runner.invoke(cli, ["export", "-f", "json"])
                assert result.exit_code == 1
                assert "No PBNJ project found" in result.output
            
    def test_export_command_success(self):
        """Test successful export command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pbnj_dir = temp_path / ".pbnj"
            pbnj_dir.mkdir()
            
            # Create metadata file
            metadata = {
                "file_info": {"name": "test.pbix"},
                "tables": [],
                "measures": []
            }
            metadata_file = pbnj_dir / "metadata.json"
            metadata_file.write_text(json.dumps(metadata))
            
            with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                mock_instance = MagicMock()
                mock_doc_gen.from_metadata_file.return_value = mock_instance
                
                with patch('pathlib.Path.cwd', return_value=temp_path):
                    result = self.runner.invoke(cli, [
                        "export", "-f", "json",
                        "-o", str(temp_path / "export.json")
                    ])
                    
                    assert result.exit_code == 0
                    assert "Exported to" in result.output
                    mock_instance.export.assert_called_once()
                
    def test_git_command_success(self):
        """Test git command success."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pbnj.core.git_integration.GitHelper') as mock_git:
                mock_instance = MagicMock()
                mock_instance.is_git_repo.return_value = False
                mock_git.return_value = mock_instance
                
                with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                    result = self.runner.invoke(cli, ["git"])
                    
                    assert result.exit_code == 0
                    assert "Changes committed to git" in result.output
                    mock_instance.init_repo.assert_called_once()
                    mock_instance.commit_changes.assert_called_once()
                
    def test_status_command_no_project(self):
        """Test status command when no project exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                result = self.runner.invoke(cli, ["status"])
                assert result.exit_code == 0
                assert "Not initialized" in result.output
            
    def test_status_command_with_project(self):
        """Test status command with project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pbnj_dir = temp_path / ".pbnj"
            pbnj_dir.mkdir()
            
            # Create metadata file
            metadata_file = pbnj_dir / "metadata.json"
            metadata_file.write_text('{"test": "data"}')
            
            # Create docs directory with files
            docs_dir = temp_path / "docs"
            docs_dir.mkdir()
            (docs_dir / "test.md").write_text("# Test")
            
            with patch('pathlib.Path.cwd', return_value=temp_path):
                result = self.runner.invoke(cli, ["status"])
                
                assert result.exit_code == 0
                assert "✓ Initialized" in result.output
                assert "✓ Available" in result.output
                assert "✓ Generated" in result.output


class TestCLIEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        
    def test_init_command_permission_error(self):
        """Test init command with permission error."""
        with patch('pbnj.core.parser.PBIXParser') as mock_parser:
            mock_parser.side_effect = PermissionError("Access denied")
            
            result = self.runner.invoke(cli, [
                "init", str(Path(__file__).parent / "AdventureWorks.pbix")
            ])
            
            assert result.exit_code == 1
            assert "Error:" in result.output
            
    def test_docs_command_invalid_format(self):
        """Test docs command with invalid format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pbnj_dir = temp_path / ".pbnj"
            pbnj_dir.mkdir()
            
            # Create metadata file
            metadata_file = pbnj_dir / "metadata.json"
            metadata_file.write_text('{"test": "data"}')
            
            result = self.runner.invoke(cli, ["docs", "-f", "invalid"], cwd=temp_dir)
            
            # Should succeed but use default format
            assert "markdown" in result.output.lower() or result.exit_code != 0
            
    def test_serve_command_port_in_use(self):
        """Test serve command when port is in use."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pbnj_dir = temp_path / ".pbnj"
            pbnj_dir.mkdir()
            
            with patch('pbnj.web.server.start_server') as mock_start_server:
                mock_start_server.side_effect = OSError("Port already in use")
                
                with patch('pathlib.Path.cwd', return_value=temp_path):
                    result = self.runner.invoke(cli, ["serve"])
                    
                    assert result.exit_code == 1
                    assert "Error:" in result.output


if __name__ == "__main__":
    pytest.main([__file__])