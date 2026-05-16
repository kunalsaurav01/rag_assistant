from langchain_community.tools.tavily_search import TavilySearchResults
from app.graph.state import GraphState
from app.utils.config import settings
from app.utils.logger import logger

def web_search_node(state: GraphState) -> GraphState:
    logger.info("--- NODE: WEB SEARCH ---")
    question = state["question"]
    
    if not settings.TAVILY_API_KEY:
        logger.warning("No TAVILY_API_KEY found, skipping web search")
        return {**state, "web_search_results": "No web search results available (API key missing)."}

    web_search_tool = TavilySearchResults(k=3)
    results = web_search_tool.invoke({"query": question})
    
    search_content = "\n".join([r["content"] for r in results])
    
    return {
        **state,
        "web_search_results": search_content
    }
