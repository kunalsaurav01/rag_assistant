import os
import httpx
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader
from langchain_core.documents import Document
from app.services.vectorstore_service import vector_service
from app.utils.config import settings
from app.utils.logger import logger

class IngestionPipeline:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def ingest_url(self, url: str):
        logger.info(f"Ingesting URL: {url}")
        try:
            response = httpx.get(url, follow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
                
            text = soup.get_text()
            # Clean whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            doc = Document(page_content=text, metadata={"source": url})
            return self._process_documents([doc])
        except Exception as e:
            logger.error(f"Error ingesting URL {url}: {e}")
            return 0

    def ingest_text(self, content: str, source_name: str):
        doc = Document(page_content=content, metadata={"source": source_name})
        return self._process_documents([doc])

    def _process_documents(self, documents):
        logger.info(f"Splitting {len(documents)} documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks.")
        vector_service.add_documents(chunks)
        return len(chunks)

ingestion_pipeline = IngestionPipeline()
