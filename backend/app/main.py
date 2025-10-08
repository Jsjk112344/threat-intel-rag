from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import QueryRequest, QueryResponse, IngestRequest, IngestResponse
from app.services.ingestion import NVDIngestionService
from app.services.rag import RAGService
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Threat Intelligence RAG API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ingestion_service = NVDIngestionService()
rag_service = RAGService()

@app.get("/")
def read_root():
    return {"message": "Threat Intelligence RAG API", "status": "running"}

@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_cves(request: IngestRequest):
    """Ingest CVEs from NVD API"""
    try:
        cves = ingestion_service.fetch_recent_cves(
            days_back=request.days_back,
            max_results=request.max_results
        )
        
        if cves:
            rag_service.ingest_cves(cves)
            return IngestResponse(
                message="CVEs ingested successfully",
                count=len(cves)
            )
        else:
            return IngestResponse(
                message="No CVEs found",
                count=0
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query", response_model=QueryResponse)
async def query_threats(request: QueryRequest):
    """Query threat intelligence"""
    try:
        result = rag_service.query(request.query)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}