from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Source(BaseModel):
    content: str
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    query_rewrite: Optional[str] = None
    retry_count: int

class IngestResponse(BaseModel):
    status: str
    message: str
    num_chunks: int

class DocumentInfo(BaseModel):
    id: str
    source: str
    metadata: Dict[str, Any]
