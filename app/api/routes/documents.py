from fastapi import APIRouter
from app.models.response_models import DocumentInfo
from app.services.vectorstore_service import vector_service
from typing import List

router = APIRouter()

@router.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    # Chroma doesn't have a simple "list all" with full metadata easily but we can get it from the collection
    collection = vector_service.get_vectorstore()._collection
    results = collection.get()
    
    docs = []
    if results and 'ids' in results:
        for i in range(len(results['ids'])):
            docs.append(DocumentInfo(
                id=results['ids'][i],
                source=results['metadatas'][i].get('source', 'unknown'),
                metadata=results['metadatas'][i]
            ))
    return docs
