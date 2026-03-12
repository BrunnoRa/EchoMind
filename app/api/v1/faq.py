from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.faq import FAQCreate, FAQUpdate, FAQResponse, FAQAskRequest, FAQAskResponse
from app.services.faq_service import FAQService

router = APIRouter(prefix="/faqs", tags=["FAQ Management"])


# ─── Rotas PÚBLICAS (usadas pelo totem sem autenticação) ──────────────────────

@router.get("/", response_model=List[FAQResponse])
async def list_faqs(db: AsyncSession = Depends(get_db)):
    """Lista todos os FAQs. Público."""
    return await FAQService.get_all(db)


@router.get("/{faq_id}", response_model=FAQResponse)
async def get_faq(faq_id: str, db: AsyncSession = Depends(get_db)):
    """Retorna um FAQ pelo ID. Público."""
    return await FAQService.get_by_id(db, faq_id)


@router.post("/ask", response_model=FAQAskResponse)
async def ask_question(body: FAQAskRequest, db: AsyncSession = Depends(get_db)):
    """Endpoint principal do totem: pergunta em texto, resposta da IA. Público."""
    return await FAQService.ask_question(db, body.question)


# ─── Rotas PROTEGIDAS (painel admin) ─────────────────────────────────────────

@router.post("/", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
async def create_faq(
    faq_in: FAQCreate,
    db: AsyncSession = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Cria um novo FAQ.  Requer autenticação."""
    return await FAQService.create_faq(db, faq_in)


@router.put("/{faq_id}", response_model=FAQResponse)
async def update_faq(
    faq_id: str,
    faq_in: FAQUpdate,
    db: AsyncSession = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Atualiza um FAQ.  Requer autenticação."""
    return await FAQService.update_faq(db, faq_id, faq_in)


@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faq(
    faq_id: str,
    db: AsyncSession = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Deleta um FAQ.  Requer autenticação."""
    await FAQService.delete_faq(db, faq_id)
