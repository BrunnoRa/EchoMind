from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.unanswered import UnansweredQuestion
from app.schemas.unanswered import UnansweredResponse

router = APIRouter(prefix="/unanswered", tags=["Unanswered Questions"])

@router.get("/", response_model=List[UnansweredResponse])
async def get_unanswered(db: AsyncSession = Depends(get_db)):
    stmt = select(UnansweredQuestion).where(UnansweredQuestion.resolved == False)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.patch("/{question_id}/resolve")
async def resolve_question(question_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(UnansweredQuestion).where(UnansweredQuestion.id == question_id)
    result = await db.execute(stmt)
    question = result.scalar_one_or_none()
    if question:
        question.resolved = True
        await db.commit()
    return {"status": "resolved"}
