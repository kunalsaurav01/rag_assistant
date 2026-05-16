from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from app.services.llm_service import get_llm
from app.graph.state import GraphState
from app.utils.logger import logger

class QueryAnalysis(BaseModel):
    rewritten_query: str = Field(description="The improved and expanded user query")
    query_type: str = Field(description="Classification: conceptual, troubleshooting, API reference, or how-to")

def query_analysis_node(state: GraphState) -> GraphState:
    logger.info("--- NODE: QUERY ANALYSIS ---")
    question = state["question"]
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical documentation expert. Your task is to analyze the user's query, "
                   "expand it for better vector search retrieval, and classify its type. "
                   "Classification must be one of: conceptual, troubleshooting, API reference, how-to."),
        ("human", "Analyze this query: {question}")
    ])
    
    # Use structured output for analysis
    chain = prompt | llm.with_structured_output(QueryAnalysis)
    result = chain.invoke({"question": question})
    
    return {
        **state,
        "question": result.rewritten_query,
        "query_type": result.query_type
    }
