from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.utils.config import settings
from app.utils.logger import logger

def get_llm(temperature=0, model="gemini-1.5-flash"):
    """
    Factory function to get the LLM based on available settings.
    """
    if settings.GEMINI_API_KEY:
        logger.info(f"Initializing Gemini LLM with model {model}")
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=temperature
        )
    elif settings.OPENAI_API_KEY:
        logger.info("Initializing OpenAI LLM")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature
        )
    else:
        raise ValueError("No LLM API key provided in environment variables")
