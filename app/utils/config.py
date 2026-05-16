import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    # LLM Settings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY")
    
    # Vector DB
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./vectorstore")
    
    # RAG Config
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 200))
    RETRY_LIMIT: int = int(os.getenv("RETRY_LIMIT", 3))
    
    # App Config
    APP_PORT: int = int(os.getenv("APP_PORT", 3000))
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
