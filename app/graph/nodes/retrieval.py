from app.services.vectorstore_service import vector_service
from app.graph.state import GraphState
from app.utils.logger import logger

def retrieval_node(state: GraphState) -> GraphState:
    logger.info("--- NODE: RETRIEVAL ---")
    question = state["question"]
    
    # Retrieve top-k chunks
    documents = vector_service.search(question, k=4)
    
    return {
        **state,
        "documents": documents
    }
