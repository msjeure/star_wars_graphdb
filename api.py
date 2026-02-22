"""
FastAPI Backend for Star Wars GraphDB
Provides REST API for the agent system
"""

import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from dotenv import load_dotenv

from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Star Wars GraphDB API",
    description="Natural Language Query Engine for Star Wars RDF Data",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global database and agent (initialized on startup)
db = None
agent = None

# ============================================================================
# Data Models
# ============================================================================

class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    question: str


class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    question: str
    sparql_query: str
    results: List[Dict]
    result_count: int


class StatsResponse(BaseModel):
    """Response model for stats endpoint"""
    total_triples: int
    total_entities: int
    total_relations: int
    entity_types: Dict[str, int]


class SchemaResponse(BaseModel):
    """Response model for schema endpoint"""
    classes: List[str]
    properties: List[str]
    sample_data: Dict


class CapabilitiesResponse(BaseModel):
    """Response model for capabilities endpoint"""
    supported_queries: List[str]
    available_commands: List[str]
    entity_types: List[str]
    total_data_points: int


# ============================================================================
# Startup and Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database and agent on startup"""
    global db, agent
    
    logger.info("Starting up Star Wars GraphDB API...")
    
    current_dir = Path(__file__).parent
    ttl_path = current_dir / "SWAPI-WD-data.ttl"
    
    if not ttl_path.exists():
        logger.error(f"TTL file not found at {ttl_path}")
        raise FileNotFoundError(f"TTL file not found: {ttl_path}")
    
    logger.info("Loading RDF graph...")
    db = initialize_db(str(ttl_path))
    
    logger.info("Initializing agent...")
    model = os.getenv("SWAPI_MODEL", "gpt-4")
    agent = StarWarsGraphAgent(db, model=model)
    
    logger.info("✅ API ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Star Wars GraphDB API...")


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "loaded" if db else "not loaded",
        "agent": "ready" if agent else "not ready"
    }


# ============================================================================
# Main Query Endpoint
# ============================================================================

@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the Star Wars knowledge graph with natural language
    
    Args:
        request: QueryRequest with 'question' field
        
    Returns:
        QueryResponse with SPARQL query and results
    """
    if not agent or not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Generate SPARQL and get results
        sparql_query, results = agent.query(request.question)
        
        return QueryResponse(
            question=request.question,
            sparql_query=sparql_query,
            results=results,
            result_count=len(results)
        )
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Information Endpoints
# ============================================================================

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get graph statistics"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    try:
        stats = db.get_graph_stats()
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/schema", response_model=SchemaResponse)
async def get_schema():
    """Get graph schema (classes and properties)"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    try:
        schema = db.get_graph_schema()
        return SchemaResponse(**schema)
    except Exception as e:
        logger.error(f"Schema error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/capabilities", response_model=CapabilitiesResponse)
async def get_capabilities():
    """Get system capabilities"""
    if not db or not agent:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        stats = db.get_graph_stats()
        
        return CapabilitiesResponse(
            supported_queries=[
                "Character information",
                "Relationships between entities",
                "Property lookups",
                "Filtering by type",
                "Aggregation queries",
                "Comparisons",
                "Complex multi-entity queries"
            ],
            available_commands=[
                "Query natural language questions",
                "View statistics",
                "View schema",
                "View this information"
            ],
            entity_types=sorted(stats["entity_types"].keys()),
            total_data_points=stats["total_triples"]
        )
    except Exception as e:
        logger.error(f"Capabilities error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Search Endpoint
# ============================================================================

@app.get("/api/search/{label}")
async def search(label: str):
    """Search for entities by label"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    if not label or len(label.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search term must be at least 2 characters")
    
    try:
        results = db.find_by_label(label)
        return {
            "search_term": label,
            "results": [
                {"uri": uri, "label": lbl}
                for uri, lbl in results[:20]  # Limit to 20 results
            ],
            "result_count": len(results)
        }
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Entity Details Endpoint
# ============================================================================

@app.get("/api/entity/{entity_id}")
async def get_entity_details(entity_id: str):
    """Get detailed properties of an entity"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    try:
        # Build full URI
        uri = f"https://swapi.co/resource/{entity_id}"
        properties = db.get_entity_properties(uri)
        
        if not properties:
            raise HTTPException(status_code=404, detail=f"Entity not found: {entity_id}")
        
        return {
            "entity_id": entity_id,
            "uri": uri,
            "properties": properties
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Entity details error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SPARQL Endpoint (for advanced users)
# ============================================================================

@app.post("/api/sparql")
async def execute_sparql(request: Dict):
    """Execute raw SPARQL query"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    if "query" not in request:
        raise HTTPException(status_code=400, detail="SPARQL query required")
    
    try:
        results = db.execute_sparql(request["query"])
        return {
            "query": request["query"],
            "results": results,
            "result_count": len(results)
        }
    except Exception as e:
        logger.error(f"SPARQL error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Frontend Routes
# ============================================================================

@app.get("/")
async def read_root():
    """Serve the main page"""
    return FileResponse("static/index.html")


@app.get("/api/docs")
async def api_docs():
    """Interactive API documentation (Swagger UI)"""
    return FileResponse("static/docs.html")


# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
