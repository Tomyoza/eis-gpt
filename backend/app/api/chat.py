# backend/app/api/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import RagService

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/question")
async def chat(request: ChatRequest):
    rag_service = RagService()
    
    try:
        response = rag_service.query(request.question)
        
        return {
            "answer": response["answer"],
            "sources": response["sources"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))