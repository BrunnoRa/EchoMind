from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.faq import FAQ
from app.schemas.faq import FAQCreate
from app.services.embedding_service import EmbeddingService

class FAQService:
    @staticmethod
    async def create_faq(db: AsyncSession, faq_in: FAQCreate):
        embedding = await EmbeddingService.get_embedding(faq_in.question)
        new_faq = FAQ(
            question=faq_in.question,
            answer=faq_in.answer,
            embedding=embedding
        )
        db.add(new_faq)
        await db.commit()
        await db.refresh(new_faq)
        return new_faq

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(FAQ))
        return result.scalars().all()
    