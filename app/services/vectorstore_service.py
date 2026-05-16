import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.utils.config import settings
from app.utils.logger import logger

class VectorStoreService:
    _instance = None
    _vectorstore = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStoreService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(cls):
        logger.info("Initializing Embeddings Model...")
        # Use a lightweight, high-performance model
        cls.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        if not os.path.exists(settings.CHROMA_DB_PATH):
            os.makedirs(settings.CHROMA_DB_PATH)
            
        logger.info(f"Initializing ChromaDB at {settings.CHROMA_DB_PATH}")
        cls._vectorstore = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=cls.embeddings
        )

    def get_vectorstore(self):
        return self._vectorstore

    def add_documents(self, documents):
        logger.info(f"Adding {len(documents)} documents to vector store")
        self._vectorstore.add_documents(documents)
        self._vectorstore.persist()
        return len(documents)

    def search(self, query, k=4):
        logger.info(f"Searching for: {query}")
        return self._vectorstore.similarity_search(query, k=k)

vector_service = VectorStoreService()
