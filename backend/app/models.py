from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str

class Source(BaseModel):
    cve_id: str
    severity: str
    cvss_score: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]

class IngestRequest(BaseModel):
    days_back: int = 30
    max_results: int = 100

class IngestResponse(BaseModel):
    message: str
    count: int