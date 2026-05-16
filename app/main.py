from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api.routes import query, ingest, documents, feedback
from app.utils.logger import logger
from app.utils.config import settings

app = FastAPI(
    title="DocuMind AI API",
    description="Backend for Self-Corrective RAG Documentation Assistant",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(ingest.router, prefix="/api", tags=["Ingest"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])

# Serve Static Files (Vite Frontend)
if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")
else:
    logger.warning("Dist folder not found, static files will not be served")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.APP_HOST}:{settings.APP_PORT}")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
