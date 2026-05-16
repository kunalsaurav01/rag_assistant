from fastapi import APIRouter, HTTPException
from app.models.request_models import IngestRequest
from app.models.response_models import IngestResponse
from app.ingestion.pipeline import ingestion_pipeline
from app.utils.logger import logger

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_content(request: IngestRequest):
    total_chunks = 0
    
    if request.urls:
        for url in request.urls:
            total_chunks += ingestion_pipeline.ingest_url(str(url))
            
    if not request.urls:
         raise HTTPException(status_code=400, detail="No sources provided for ingestion")
         
    return IngestResponse(
        status="success",
        message=f"Successfully ingested content",
        num_chunks=total_chunks
    )
