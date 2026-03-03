from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.interaction import Interaction
from app.models.faq import FAQ

class MetricsService:
    @staticmethod
    async def get_overview(db: AsyncSession):
        total_interactions = await db.execute(select(func.count(Interaction.id)))
        avg_time = await db.execute(select(func.avg(Interaction.response_time)))
        
        return {
            "total_queries": total_interactions.scalar(),
            "avg_response_time": round(avg_time.scalar() or 0, 2)
        }

    @staticmethod
    async def get_top_faqs(db: AsyncSession, limit: int = 5):
        # Simplificado: retorna os últimos FAQs criados como "top" 
        # para fins de exemplo de estrutura
        stmt = select(FAQ).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
    