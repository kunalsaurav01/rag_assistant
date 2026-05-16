from fastapi import APIRouter
from app.models.request_models import FeedbackRequest
from app.utils.logger import logger

router = APIRouter()

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    logger.info(f"Feedback received for query {request.query_id}: vote={request.vote}, comment={request.comment}")
    # In a real production app, you'd save this to a SQL DB for later analysis and fine-tuning
    return {"status": "success", "message": "Thank you for your feedback!"}
