"""FastAPI web server for PBNJ."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from pbnj.core.parser import PBIXParser
from pbnj.docs.generator import DocumentationGenerator


class ProjectInfo(BaseModel):
    """Project information model."""
    name: str
    file_size_mb: float
    table_count: int
    measure_count: int
    relationship_count: int
    power_query_count: int


class PBIXUploadResponse(BaseModel):
    """Response model for PBIX upload."""
    success: bool
    message: str
    project_info: Optional[ProjectInfo] = None


# Create FastAPI app
app = FastAPI(
    title="PBNJ - Power BI Documentation Tool",
    description="Transform .pbix files into readable, AI-friendly documentation",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
current_project_path: Optional[Path] = None
current_metadata: Optional[Dict[str, Any]] = None


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "PBNJ API Server", "version": "0.1.0"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/upload", response_model=PBIXUploadResponse)
async def upload_pbix(file: UploadFile = File(...)) -> PBIXUploadResponse:
    """Upload and parse a PBIX file."""
    global current_project_path, current_metadata
    
    if not file.filename or not file.filename.endswith('.pbix'):
        raise HTTPException(status_code=400, detail="File must be a .pbix file")
    
    try:
        # Save uploaded file temporarily
        temp_dir = Path.cwd() / ".pbnj" / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        temp_file = temp_dir / file.filename
        content = await file.read()
        temp_file.write_bytes(content)
        
        # Parse the PBIX file
        parser = PBIXParser(temp_file)
        metadata = parser.extract_metadata()
        
        # Update global state
        current_project_path = Path.cwd()
        current_metadata = metadata
        
        # Save metadata
        metadata_file = Path.cwd() / ".pbnj" / "metadata.json"
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)
        
        # Generate documentation
        doc_gen = DocumentationGenerator(metadata, Path.cwd())
        doc_gen.generate_all()
        
        # Create project info
        project_info = ProjectInfo(
            name=metadata["file_info"]["name"],
            file_size_mb=round(metadata["file_info"]["size_bytes"] / (1024 * 1024), 2),
            table_count=len(metadata.get("tables", [])),
            measure_count=len(metadata.get("measures", [])),
            relationship_count=len(metadata.get("relationships", [])),
            power_query_count=len(metadata.get("power_query", {}).get("queries", [])),
        )
        
        # Clean up temp file
        temp_file.unlink(missing_ok=True)
        
        return PBIXUploadResponse(
            success=True,
            message="PBIX file processed successfully",
            project_info=project_info,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PBIX file: {str(e)}")


@app.get("/api/project/info")
async def get_project_info() -> Dict[str, Any]:
    """Get current project information."""
    if current_metadata is None:
        raise HTTPException(status_code=404, detail="No project loaded")
    
    return {
        "file_info": current_metadata["file_info"],
        "summary": {
            "table_count": len(current_metadata.get("tables", [])),
            "measure_count": len(current_metadata.get("measures", [])),
            "relationship_count": len(current_metadata.get("relationships", [])),
            "power_query_count": len(current_metadata.get("power_query", {}).get("queries", [])),
        },
    }


@app.get("/api/project/metadata")
async def get_metadata() -> Dict[str, Any]:
    """Get full project metadata."""
    if current_metadata is None:
        # Try to load from file
        metadata_file = Path.cwd() / ".pbnj" / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                current_metadata = json.load(f)
        else:
            raise HTTPException(status_code=404, detail="No project found")
    
    return current_metadata


@app.get("/api/tables")
async def get_tables() -> List[Dict[str, Any]]:
    """Get tables information."""
    metadata = await get_metadata()
    return metadata.get("tables", [])


@app.get("/api/measures")
async def get_measures() -> List[Dict[str, Any]]:
    """Get measures information."""
    metadata = await get_metadata()
    return metadata.get("measures", [])


@app.get("/api/relationships")
async def get_relationships() -> List[Dict[str, Any]]:
    """Get relationships information."""
    metadata = await get_metadata()
    return metadata.get("relationships", [])


@app.get("/api/power-query")
async def get_power_query() -> Dict[str, Any]:
    """Get Power Query information."""
    metadata = await get_metadata()
    return metadata.get("power_query", {})


@app.get("/api/export/{format}")
async def export_documentation(format: str) -> FileResponse:
    """Export documentation in specified format."""
    if current_metadata is None:
        raise HTTPException(status_code=404, detail="No project loaded")
    
    if format not in ["json", "markdown"]:
        raise HTTPException(status_code=400, detail="Unsupported export format")
    
    try:
        output_file = Path.cwd() / f"export.{format}"
        
        doc_gen = DocumentationGenerator(current_metadata, Path.cwd())
        doc_gen.export(format, output_file)
        
        return FileResponse(
            path=output_file,
            filename=f"pbnj_export.{format}",
            media_type="application/octet-stream",
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.get("/api/documentation/{doc_type}")
async def get_documentation(doc_type: str) -> Dict[str, str]:
    """Get specific documentation content."""
    docs_dir = Path.cwd() / "docs"
    
    doc_files = {
        "readme": Path.cwd() / "README.md",
        "tables": docs_dir / "tables.md",
        "measures": docs_dir / "measures.md",
        "power-query": docs_dir / "power_query.md",
        "relationships": docs_dir / "relationships.md",
        "technical": docs_dir / "technical.md",
        "business": docs_dir / "business.md",
        "summary": docs_dir / "summary.md",
    }
    
    if doc_type not in doc_files:
        raise HTTPException(status_code=404, detail="Documentation type not found")
    
    doc_file = doc_files[doc_type]
    if not doc_file.exists():
        raise HTTPException(status_code=404, detail="Documentation file not found")
    
    content = doc_file.read_text(encoding="utf-8")
    return {"content": content, "type": doc_type}


# Serve static files for frontend (when React app is built)
frontend_dist = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dist / "static")), name="static")
    
    @app.get("/app/{path:path}")
    async def serve_frontend(path: str) -> FileResponse:
        """Serve React frontend."""
        return FileResponse(frontend_dist / "index.html")
    
    @app.get("/app")
    async def serve_frontend_root() -> FileResponse:
        """Serve React frontend root."""
        return FileResponse(frontend_dist / "index.html")


def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
    """Start the FastAPI server."""
    uvicorn.run(
        "pbnj.web.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )