"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_directory():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_pbix_path():
    """Provide path to sample PBIX file."""
    return Path(__file__).parent / "AdventureWorks.pbix"


@pytest.fixture
def sample_metadata():
    """Provide sample metadata for testing."""
    return {
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


# Mark slow tests
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")