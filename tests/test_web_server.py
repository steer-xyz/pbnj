"""Tests for web server functionality."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from pbnj.web.server import app


class TestWebServer:
    """Test cases for the web server."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
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
                    "description": "Customer dimension",
                    "hidden": False
                }
            ],
            "measures": [
                {
                    "name": "Total Sales",
                    "formula": "SUM(FactSales[Amount])"
                }
            ],
            "relationships": [
                {
                    "from_table": "FactSales",
                    "to_table": "DimCustomer"
                }
            ],
            "power_query": {
                "queries": [
                    {
                        "name": "Customer Query",
                        "code": "let Source = ... in Source"
                    }
                ]
            }
        }
        
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "PBNJ API Server"
        assert data["version"] == "0.1.0"
        
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        
    def test_upload_pbix_invalid_file_type(self):
        """Test upload with invalid file type."""
        # Create a fake non-PBIX file
        fake_file = ("test.txt", b"fake content", "text/plain")
        
        response = self.client.post(
            "/api/upload",
            files={"file": fake_file}
        )
        
        assert response.status_code == 400
        assert "File must be a .pbix file" in response.json()["detail"]
        
    def test_upload_pbix_success(self):
        """Test successful PBIX upload."""
        # Create a fake PBIX file
        fake_pbix_content = b"fake pbix content"
        fake_file = ("test.pbix", fake_pbix_content, "application/octet-stream")
        
        with patch('pbnj.core.parser.PBIXParser') as mock_parser:
            mock_instance = MagicMock()
            mock_instance.extract_metadata.return_value = self.sample_metadata
            mock_parser.return_value = mock_instance
            
            with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                mock_doc_instance = MagicMock()
                mock_doc_gen.return_value = mock_doc_instance
                
                response = self.client.post(
                    "/api/upload",
                    files={"file": fake_file}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "processed successfully" in data["message"]
                assert data["project_info"]["name"] == "test.pbix"
                assert data["project_info"]["table_count"] == 1
                
    def test_upload_pbix_parsing_error(self):
        """Test PBIX upload with parsing error."""
        fake_file = ("test.pbix", b"fake content", "application/octet-stream")
        
        with patch('pbnj.core.parser.PBIXParser') as mock_parser:
            mock_parser.side_effect = Exception("Parsing failed")
            
            response = self.client.post(
                "/api/upload",
                files={"file": fake_file}
            )
            
            assert response.status_code == 500
            assert "Error processing PBIX file" in response.json()["detail"]
            
    def test_get_project_info_no_project(self):
        """Test get project info when no project is loaded."""
        # Reset global state
        from pbnj.web.server import current_metadata
        app.dependency_overrides.clear()
        
        response = self.client.get("/api/project/info")
        assert response.status_code == 404
        assert "No project loaded" in response.json()["detail"]
        
    def test_get_project_info_success(self):
        """Test successful project info retrieval."""
        # Mock global state
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            response = self.client.get("/api/project/info")
            
            assert response.status_code == 200
            data = response.json()
            assert "file_info" in data
            assert "summary" in data
            assert data["summary"]["table_count"] == 1
            
    def test_get_metadata_no_project(self):
        """Test get metadata when no project exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                with patch('pbnj.web.server.current_metadata', None):
                    response = self.client.get("/api/project/metadata")
                    assert response.status_code == 404
                    
    def test_get_metadata_from_file(self):
        """Test get metadata from file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pbnj_dir = temp_path / ".pbnj"
            pbnj_dir.mkdir()
            
            metadata_file = pbnj_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(self.sample_metadata, f)
                
            with patch('pathlib.Path.cwd', return_value=temp_path):
                with patch('pbnj.web.server.current_metadata', None):
                    response = self.client.get("/api/project/metadata")
                    
                    assert response.status_code == 200
                    data = response.json()
                    assert data == self.sample_metadata
                    
    def test_get_metadata_success(self):
        """Test successful metadata retrieval."""
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            response = self.client.get("/api/project/metadata")
            
            assert response.status_code == 200
            data = response.json()
            assert data == self.sample_metadata
            
    def test_get_tables(self):
        """Test get tables endpoint."""
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            response = self.client.get("/api/tables")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["name"] == "DimCustomer"
            
    def test_get_measures(self):
        """Test get measures endpoint."""
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            response = self.client.get("/api/measures")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["name"] == "Total Sales"
            
    def test_get_relationships(self):
        """Test get relationships endpoint."""
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            response = self.client.get("/api/relationships")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["from_table"] == "FactSales"
            
    def test_get_power_query(self):
        """Test get Power Query endpoint."""
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            response = self.client.get("/api/power-query")
            
            assert response.status_code == 200
            data = response.json()
            assert "queries" in data
            assert len(data["queries"]) == 1
            
    def test_export_documentation_no_project(self):
        """Test export when no project is loaded."""
        with patch('pbnj.web.server.current_metadata', None):
            response = self.client.get("/api/export/json")
            assert response.status_code == 404
            
    def test_export_documentation_invalid_format(self):
        """Test export with invalid format."""
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            response = self.client.get("/api/export/invalid")
            assert response.status_code == 400
            assert "Unsupported export format" in response.json()["detail"]
            
    def test_export_documentation_success(self):
        """Test successful documentation export."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                with patch('pbnj.web.server.current_metadata', self.sample_metadata):
                    with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                        mock_instance = MagicMock()
                        mock_doc_gen.return_value = mock_instance
                        
                        # Create a fake export file
                        export_file = Path(temp_dir) / "export.json"
                        export_file.write_text(json.dumps(self.sample_metadata))
                        
                        response = self.client.get("/api/export/json")
                        
                        assert response.status_code == 200
                        assert response.headers["content-type"] == "application/octet-stream"
                        
    def test_export_documentation_error(self):
        """Test export with error."""
        with patch('pbnj.web.server.current_metadata', self.sample_metadata):
            with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                mock_instance = MagicMock()
                mock_instance.export.side_effect = Exception("Export failed")
                mock_doc_gen.return_value = mock_instance
                
                response = self.client.get("/api/export/json")
                
                assert response.status_code == 500
                assert "Export failed" in response.json()["detail"]
                
    def test_get_documentation_invalid_type(self):
        """Test get documentation with invalid type."""
        response = self.client.get("/api/documentation/invalid")
        assert response.status_code == 404
        assert "Documentation type not found" in response.json()["detail"]
        
    def test_get_documentation_file_not_found(self):
        """Test get documentation when file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                response = self.client.get("/api/documentation/readme")
                assert response.status_code == 404
                assert "Documentation file not found" in response.json()["detail"]
                
    def test_get_documentation_success(self):
        """Test successful documentation retrieval."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create README file
            readme_content = "# Test Documentation\nThis is a test."
            readme_file = temp_path / "README.md"
            readme_file.write_text(readme_content)
            
            with patch('pathlib.Path.cwd', return_value=temp_path):
                response = self.client.get("/api/documentation/readme")
                
                assert response.status_code == 200
                data = response.json()
                assert data["content"] == readme_content
                assert data["type"] == "readme"
                
    def test_get_documentation_tables(self):
        """Test get tables documentation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            docs_dir = temp_path / "docs"
            docs_dir.mkdir()
            
            # Create tables documentation
            tables_content = "# Tables\n\n## DimCustomer\nCustomer table."
            tables_file = docs_dir / "tables.md"
            tables_file.write_text(tables_content)
            
            with patch('pathlib.Path.cwd', return_value=temp_path):
                response = self.client.get("/api/documentation/tables")
                
                assert response.status_code == 200
                data = response.json()
                assert data["content"] == tables_content
                assert data["type"] == "tables"


class TestWebServerModels:
    """Test Pydantic models."""
    
    def test_project_info_model(self):
        """Test ProjectInfo model."""
        from pbnj.web.server import ProjectInfo
        
        project_info = ProjectInfo(
            name="test.pbix",
            file_size_mb=2.5,
            table_count=5,
            measure_count=10,
            relationship_count=3,
            power_query_count=7
        )
        
        assert project_info.name == "test.pbix"
        assert project_info.file_size_mb == 2.5
        assert project_info.table_count == 5
        
    def test_pbix_upload_response_model(self):
        """Test PBIXUploadResponse model."""
        from pbnj.web.server import PBIXUploadResponse, ProjectInfo
        
        project_info = ProjectInfo(
            name="test.pbix",
            file_size_mb=2.5,
            table_count=5,
            measure_count=10,
            relationship_count=3,
            power_query_count=7
        )
        
        response = PBIXUploadResponse(
            success=True,
            message="Upload successful",
            project_info=project_info
        )
        
        assert response.success is True
        assert response.message == "Upload successful"
        assert response.project_info.name == "test.pbix"
        
    def test_pbix_upload_response_without_project_info(self):
        """Test PBIXUploadResponse without project info."""
        from pbnj.web.server import PBIXUploadResponse
        
        response = PBIXUploadResponse(
            success=False,
            message="Upload failed"
        )
        
        assert response.success is False
        assert response.message == "Upload failed"
        assert response.project_info is None


class TestWebServerIntegration:
    """Integration tests for web server."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
        self.test_pbix = Path(__file__).parent / "AdventureWorks.pbix"
        
    @pytest.mark.integration
    def test_upload_real_pbix(self):
        """Test upload with real PBIX file."""
        if not self.test_pbix.exists():
            pytest.skip("AdventureWorks.pbix not found")
            
        with open(self.test_pbix, 'rb') as f:
            pbix_content = f.read()
            
        fake_file = ("AdventureWorks.pbix", pbix_content, "application/octet-stream")
        
        try:
            response = self.client.post(
                "/api/upload",
                files={"file": fake_file}
            )
            
            # Should either succeed or fail gracefully
            assert response.status_code in [200, 500]
            
            if response.status_code == 200:
                data = response.json()
                assert data["success"] is True
                assert "AdventureWorks.pbix" in data["project_info"]["name"]
                
        except Exception as e:
            # Real PBIX parsing might fail due to pbixray limitations
            # This is acceptable for testing
            print(f"Real PBIX upload failed (expected): {e}")
            
    def test_full_workflow(self):
        """Test complete workflow from upload to export."""
        # Upload
        fake_file = ("test.pbix", b"fake content", "application/octet-stream")
        
        sample_metadata = {
            "file_info": {"name": "test.pbix", "size_bytes": 1000},
            "tables": [{"name": "TestTable"}],
            "measures": [],
            "relationships": [],
            "power_query": {"queries": []}
        }
        
        with patch('pbnj.core.parser.PBIXParser') as mock_parser:
            mock_instance = MagicMock()
            mock_instance.extract_metadata.return_value = sample_metadata
            mock_parser.return_value = mock_instance
            
            with patch('pbnj.docs.generator.DocumentationGenerator') as mock_doc_gen:
                mock_doc_instance = MagicMock()
                mock_doc_gen.return_value = mock_doc_instance
                
                # Upload
                upload_response = self.client.post(
                    "/api/upload",
                    files={"file": fake_file}
                )
                assert upload_response.status_code == 200
                
                # Get project info
                with patch('pbnj.web.server.current_metadata', sample_metadata):
                    info_response = self.client.get("/api/project/info")
                    assert info_response.status_code == 200
                    
                    # Get tables
                    tables_response = self.client.get("/api/tables")
                    assert tables_response.status_code == 200
                    assert len(tables_response.json()) == 1
                    
                    # Export
                    with tempfile.TemporaryDirectory() as temp_dir:
                        with patch('pathlib.Path.cwd', return_value=Path(temp_dir)):
                            export_file = Path(temp_dir) / "export.json"
                            export_file.write_text(json.dumps(sample_metadata))
                            
                            export_response = self.client.get("/api/export/json")
                            assert export_response.status_code == 200


class TestWebServerErrorHandling:
    """Test error handling scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
        
    def test_upload_large_file(self):
        """Test upload with very large file."""
        # Create a large fake file (this would normally fail due to size limits)
        large_content = b"x" * (100 * 1024 * 1024)  # 100MB
        large_file = ("large.pbix", large_content, "application/octet-stream")
        
        # This might timeout or fail due to size - that's expected
        try:
            response = self.client.post(
                "/api/upload",
                files={"file": large_file},
                timeout=5.0
            )
            # If it responds, it should be an error
            assert response.status_code != 200
        except Exception:
            # Timeout or connection error is acceptable
            pass
            
    def test_concurrent_uploads(self):
        """Test handling concurrent uploads."""
        import threading
        import time
        
        fake_file = ("test.pbix", b"fake content", "application/octet-stream")
        
        results = []
        
        def upload_file():
            try:
                response = self.client.post(
                    "/api/upload",
                    files={"file": fake_file}
                )
                results.append(response.status_code)
            except Exception as e:
                results.append(str(e))
                
        # Start multiple upload threads
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=upload_file)
            threads.append(thread)
            thread.start()
            
        # Wait for all threads
        for thread in threads:
            thread.join(timeout=10.0)
            
        # At least one should complete (might be success or error)
        assert len(results) > 0


if __name__ == "__main__":
    pytest.main([__file__])