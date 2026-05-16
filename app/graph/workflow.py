from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.graph.state import GraphState
from app.graph.nodes.query_analysis import query_analysis_node
from app.graph.nodes.retrieval import retrieval_node
from app.graph.nodes.grading import grading_node
from app.graph.nodes.generation import generation_node
from app.graph.nodes.transform_query import transform_query_node
from app.graph.nodes.hallucination_check import hallucination_check_node
from app.graph.nodes.web_search import web_search_node
from app.utils.config import settings
from app.utils.logger import logger

def decide_to_generate(state: GraphState):
    """
    Determines whether to generate an answer or fallback to web search.
    """
    logger.info("--- DECIDING PATH: RETRIEVAL VALIDATION ---")
    documents = state.get("documents", [])
    retry_count = state.get("retry_count", 0)
    
    if not documents:
        if retry_count >= settings.RETRY_LIMIT:
            logger.info("  Decision: MAX RETRIES -> WEB SEARCH FALLBACK")
            return "web_search"
        else:
            logger.info("  Decision: NO RELEVANT DOCUMENTS -> TRANSFORM QUERY")
            return "transform_query"
    else:
        logger.info("  Decision: GENERATE")
        return "generate"

def grade_generation_v_documents(state: GraphState):
    """
    Determines if generation is acceptable or a hallucination.
    """
    logger.info("--- DECIDING PATH: HALLUCINATION CHECK ---")
    is_hallucination = state.get("is_hallucination")
    
    if is_hallucination == "no":
        logger.info("  Decision: ANSWER IS GROUNDED")
        return "useful"
    else:
        logger.info("  Decision: HALLUCINATION DETECTED -> RETRY TRANSFORM")
        return "not_useful"

def create_workflow():
    workflow = StateGraph(GraphState)
    
    # Define Nodes
    workflow.add_node("query_analysis", query_analysis_node)
    workflow.add_node("retrieve", retrieval_node)
    workflow.add_node("grade_documents", grading_node)
    workflow.add_node("generate", generation_node)
    workflow.add_node("transform_query", transform_query_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("hallucination_check", hallucination_check_node)
    
    # Build Graph Connections
    workflow.set_entry_point("query_analysis")
    
    workflow.add_edge("query_analysis", "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
            "web_search": "web_search"
        }
    )
    
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_edge("web_search", "generate")
    
    workflow.add_edge("generate", "hallucination_check")
    
    workflow.add_conditional_edges(
        "hallucination_check",
        grade_generation_v_documents,
        {
            "useful": END,
            "not_useful": "transform_query"
        }
    )
    
    # Compile with memory
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app

# Initialize the graph
rag_app = create_workflow()
