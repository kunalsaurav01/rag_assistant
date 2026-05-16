from langchain_core.prompts import ChatPromptTemplate
from app.services.llm_service import get_llm
from app.graph.state import GraphState
from app.utils.logger import logger

def transform_query_node(state: GraphState) -> GraphState:
    logger.info("--- NODE: TRANSFORM QUERY ---")
    question = state["question"]
    original_question = state["original_question"]
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a query optimizer. The current search for the user's question yielded no relevant results. "
                   "Rewrite the user's question to improve vector database retrieval. "
                   "Try to keep the core intent but simplify or clarify technical terms if necessary."),
        ("human", "Original Question: {original_question}\nFailed Query: {current_query}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"original_question": original_question, "current_query": question})
    
    return {
        **state,
        "question": result.content,
        "retry_count": state["retry_count"] + 1
    }
