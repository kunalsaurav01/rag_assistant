from typing import List, TypedDict, Dict, Any, Optional

class GraphState(TypedDict):
    """
    Represents the state of our RAG graph.
    """
    question: str
    original_question: str
    documents: List[Any]
    generation: Optional[str]
    rewrite_query: Optional[str]
    retry_count: int
    relevance_scores: List[str] # ["relevant", "irrelevant", ...]
    query_type: Optional[str] # conceptual, how-to, etc.
    sources: List[Dict[str, Any]]
    web_search_results: Optional[str]
    is_hallucination: Optional[str] # "yes", "no"
