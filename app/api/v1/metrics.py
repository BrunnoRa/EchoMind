from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/metrics", tags=["Analytics"])

@router.get("/overview")
async def get_stats(db: AsyncSession = Depends(get_db)):
    return await MetricsService.get_overview(db)
