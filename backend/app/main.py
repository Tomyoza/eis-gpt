from fastapi import FastAPI
from app.core.config import settings

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

# Development Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)