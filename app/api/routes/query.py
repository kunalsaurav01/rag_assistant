from fastapi import APIRouter, HTTPException
from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse, Source
from app.graph.workflow import rag_app
from app.utils.logger import logger

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    logger.info(f"Received query: {request.question}")
    
    try:
        # Prepare initial state
        initial_state = {
            "question": request.question,
            "original_question": request.question,
            "documents": [],
            "generation": None,
            "retry_count": 0,
            "relevance_scores": [],
            "query_type": None,
            "sources": []
        }
        
        # Execute Graph with thread_id for memory
        config = {"configurable": {"thread_id": request.thread_id}}
        result = rag_app.invoke(initial_state, config=config)
        
        if not result.get("generation"):
            return QueryResponse(
                answer="I'm sorry, I couldn't find any relevant information to answer your question after multiple attempts.",
                sources=[],
                retry_count=result.get("retry_count", 0)
            )
            
        return QueryResponse(
            answer=result["generation"],
            sources=[Source(content=s["content"], metadata=s["metadata"]) for s in result.get("sources", [])],
            query_rewrite=result.get("question") if result.get("question") != request.question else None,
            retry_count=result.get("retry_count", 0)
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
