"""Core PBIX parsing engine using pbixray."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from pbixray import PBIXRay


class PBIXParser:
    """Parser for Power BI (.pbix) files using pbixray."""
    
    def __init__(self, pbix_path: Path) -> None:
        """Initialize parser with .pbix file path."""
        self.pbix_path = pbix_path
        self.model: Optional[PBIXRay] = None
        self._metadata: Optional[Dict[str, Any]] = None
    
    def _load_model(self) -> PBIXRay:
        """Load the PBIX model using pbixray."""
        if self.model is None:
            self.model = PBIXRay(str(self.pbix_path))
        return self.model
    
    def extract_metadata(self) -> Dict[str, Any]:
        """Extract all metadata from the PBIX file."""
        if self._metadata is not None:
            return self._metadata
        
        model = self._load_model()
        
        self._metadata = {
            "file_info": {
                "name": self.pbix_path.name,
                "path": str(self.pbix_path),
                "size_bytes": self.pbix_path.stat().st_size,
            },
            "tables": self._extract_tables(model),
            "relationships": self._extract_relationships(model),
            "measures": self._extract_measures(model),
            "calculated_columns": self._extract_calculated_columns(model),
            "power_query": self._extract_power_query(model),
            "parameters": self._extract_parameters(model),
            "metadata": self._extract_model_metadata(model),
        }
        
        return self._metadata
    
    def _extract_tables(self, model: PBIXRay) -> List[Dict[str, Any]]:
        """Extract table information."""
        try:
            tables_df = model.tables
            tables = []
            
            for _, table in tables_df.iterrows():
                table_info = {
                    "name": table.get("Name", ""),
                    "type": table.get("Type", ""),
                    "description": table.get("Description", ""),
                    "hidden": table.get("IsHidden", False),
                    "columns": self._extract_table_columns(model, table.get("Name", "")),
                }
                tables.append(table_info)
            
            return tables
        except Exception as e:
            return [{"error": f"Failed to extract tables: {str(e)}"}]
    
    def _extract_table_columns(self, model: PBIXRay, table_name: str) -> List[Dict[str, Any]]:
        """Extract column information for a specific table."""
        try:
            # Get columns for the specific table
            columns = []
            # Note: pbixray might have different methods to get columns
            # This is a placeholder implementation
            return columns
        except Exception:
            return []
    
    def _extract_relationships(self, model: PBIXRay) -> List[Dict[str, Any]]:
        """Extract relationship information."""
        try:
            # Extract relationships between tables
            relationships = []
            # Note: Implementation depends on pbixray API
            return relationships
        except Exception as e:
            return [{"error": f"Failed to extract relationships: {str(e)}"}]
    
    def _extract_measures(self, model: PBIXRay) -> List[Dict[str, Any]]:
        """Extract DAX measures."""
        try:
            measures = []
            # Extract DAX measures
            # Note: Implementation depends on pbixray API
            return measures
        except Exception as e:
            return [{"error": f"Failed to extract measures: {str(e)}"}]
    
    def _extract_calculated_columns(self, model: PBIXRay) -> List[Dict[str, Any]]:
        """Extract calculated columns."""
        try:
            calc_columns = []
            # Extract calculated columns
            # Note: Implementation depends on pbixray API
            return calc_columns
        except Exception as e:
            return [{"error": f"Failed to extract calculated columns: {str(e)}"}]
    
    def _extract_power_query(self, model: PBIXRay) -> Dict[str, Any]:
        """Extract Power Query M code."""
        try:
            power_query_info = {
                "queries": [],
                "parameters": [],
                "functions": [],
            }
            
            # Extract Power Query code
            pq_code = model.power_query
            if pq_code is not None:
                power_query_info["raw_code"] = str(pq_code)
                # Parse the M code to extract individual queries
                power_query_info["queries"] = self._parse_power_query_code(pq_code)
            
            return power_query_info
        except Exception as e:
            return {"error": f"Failed to extract Power Query: {str(e)}"}
    
    def _parse_power_query_code(self, pq_code: Any) -> List[Dict[str, Any]]:
        """Parse Power Query M code into structured format."""
        queries = []
        try:
            # Basic parsing of M code
            # This is a simplified implementation
            code_str = str(pq_code)
            
            # Split by "let" statements to identify queries
            sections = code_str.split("let")
            
            for i, section in enumerate(sections[1:], 1):  # Skip first empty split
                query_info = {
                    "name": f"Query_{i}",
                    "code": f"let{section}",
                    "steps": self._extract_query_steps(f"let{section}"),
                }
                queries.append(query_info)
            
        except Exception:
            pass
        
        return queries
    
    def _extract_query_steps(self, query_code: str) -> List[str]:
        """Extract individual steps from a Power Query."""
        steps = []
        try:
            # Simple step extraction
            lines = query_code.split("\n")
            for line in lines:
                line = line.strip()
                if "=" in line and not line.startswith("//"):
                    steps.append(line)
        except Exception:
            pass
        
        return steps
    
    def _extract_parameters(self, model: PBIXRay) -> List[Dict[str, Any]]:
        """Extract Power Query parameters."""
        try:
            parameters = []
            # Extract parameters
            # Note: Implementation depends on pbixray API
            return parameters
        except Exception as e:
            return [{"error": f"Failed to extract parameters: {str(e)}"}]
    
    def _extract_model_metadata(self, model: PBIXRay) -> Dict[str, Any]:
        """Extract general model metadata."""
        try:
            metadata_info = {}
            
            # Get basic metadata
            metadata = model.metadata
            if metadata is not None:
                metadata_info = metadata.to_dict() if hasattr(metadata, 'to_dict') else {}
            
            return metadata_info
        except Exception as e:
            return {"error": f"Failed to extract metadata: {str(e)}"}
    
    def save_metadata(self, output_path: Path) -> None:
        """Save extracted metadata to JSON file."""
        metadata = self.extract_metadata()
        
        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the PBIX file contents."""
        metadata = self.extract_metadata()
        
        summary = {
            "file_name": metadata["file_info"]["name"],
            "file_size_mb": round(metadata["file_info"]["size_bytes"] / (1024 * 1024), 2),
            "table_count": len(metadata.get("tables", [])),
            "measure_count": len(metadata.get("measures", [])),
            "relationship_count": len(metadata.get("relationships", [])),
            "power_query_count": len(metadata.get("power_query", {}).get("queries", [])),
        }
        
        return summary