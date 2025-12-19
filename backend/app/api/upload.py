from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag_service import RagService
import shutil
import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        rag_service = RagService()
        
        temp_filename = f"temp_{file.filename}"
        
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        num_chunks = await rag_service.ingest_file(temp_filename, file.filename)

        os.remove(temp_filename)
        
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_processed": num_chunks
        }

    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))