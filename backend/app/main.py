from fastapi import FastAPI
from app.core.config import settings
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

# Initialize the API
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A local RAG API using Ollama and ChromaDB"
)

# Health Check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "model": settings.LLM_MODEL
    }

app.include_router(upload_router, prefix="/api/documents", tags=["Documents"])

app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])

# Development Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)