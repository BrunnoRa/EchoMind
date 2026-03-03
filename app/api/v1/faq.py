from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.faq import FAQCreate, FAQResponse
from app.services.faq_service import FAQService

router = APIRouter(prefix="/faqs", tags=["FAQ Management"])

@router.post("/", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
async def create_faq(faq_in: FAQCreate, db: AsyncSession = Depends(get_db)):
    return await FAQService.create_faq(db, faq_in)

@router.get("/", response_model=List[FAQResponse])
async def list_faqs(db: AsyncSession = Depends(get_db)):
    return await FAQService.get_all(db)
