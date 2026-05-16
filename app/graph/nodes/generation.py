from langchain_core.prompts import ChatPromptTemplate
from app.services.llm_service import get_llm
from app.graph.state import GraphState
from app.utils.logger import logger

def generation_node(state: GraphState) -> GraphState:
    logger.info("--- NODE: GENERATION ---")
    documents = state["documents"]
    question = state["question"]
    web_results = state.get("web_search_results")
    llm = get_llm()
    
    # Construct context
    context = "\n\n".join([f"Source {i+1}: {doc.page_content}" for i, doc in enumerate(documents)])
    
    if web_results:
        logger.info("  Adding Web Search Results to context")
        context += f"\n\nAdditional Web Information:\n{web_results}"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical assistant. Answer the user's question accurately using the provided context. "
                   "If the context is insufficient, explain why and provide the best possible partial answer based on what's available. "
                   "Cite your source numbers [Source X] if applicable. If using web info, cite as [Web Info]."),
        ("human", "Question: {question}\n\nContext:\n{context}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"question": question, "context": context})
    
    # Extract sources for final response
    sources_metadata = [{"content": doc.page_content, "metadata": doc.metadata} for doc in documents]
    
    return {
        **state,
        "generation": result.content,
        "sources": sources_metadata
    }
