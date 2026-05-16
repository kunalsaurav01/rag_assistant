from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    question: str
    thread_id: Optional[str] = "default"

class IngestRequest(BaseModel):
    files: Optional[List[str]] = None
    urls: Optional[List[HttpUrl]] = None

class FeedbackRequest(BaseModel):
    query_id: str
    vote: int # 1 for up, -1 for down
    comment: Optional[str] = None
