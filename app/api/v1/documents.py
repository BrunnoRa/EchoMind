import os
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse

router = APIRouter(prefix="/documents", tags=["RAG Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        doc = await DocumentService.process_pdf_upload(db, temp_path, file.filename)
        return doc
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            