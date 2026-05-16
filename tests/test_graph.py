import pytest
from app.graph.workflow import rag_app
from app.graph.state import GraphState

def test_graph_initialization():
    assert rag_app is not None

def test_decide_to_generate_logic():
    from app.graph.workflow import decide_to_generate
    
    # Case 1: Has docs
    state_with_docs: GraphState = {"documents": ["doc1"], "retry_count": 0}
    assert decide_to_generate(state_with_docs) == "generate"
    
    # Case 2: No docs, under retry limit
    state_no_docs: GraphState = {"documents": [], "retry_count": 0}
    assert decide_to_generate(state_no_docs) == "transform_query"
    
    # Case 3: No docs, at retry limit
    state_max_retries: GraphState = {"documents": [], "retry_count": 3}
    assert decide_to_generate(state_max_retries) == "max_retries"
