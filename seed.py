import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.services.faq_service import FAQService
from app.schemas.faq import FAQCreate
from app.models.event import Event
from datetime import datetime, timedelta

async def seed():
    async with AsyncSessionLocal() as db:
        print("🌱 Iniciando o seed de dados...")
        
        # 1. Adicionar FAQs de exemplo
        faqs = [
            FAQCreate(question="Onde fica a secretaria?", answer="A secretaria central fica no Bloco A, térreo, funcionando das 08h às 22h."),
            FAQCreate(question="Como emitir o histórico escolar?", answer="Você pode emitir pelo portal do aluno na aba 'Documentos' ou solicitar na secretaria."),
            FAQCreate(question="Quais são as regras da biblioteca?", answer="Empréstimos de até 3 livros por 7 dias. Multa de R$ 2,00 por dia de atraso.")
        ]
        
        for faq_in in faqs:
            await FAQService.create_faq(db, faq_in)
            print(f"✅ FAQ adicionado: {faq_in.question}")

        # 2. Adicionar Eventos de exemplo
        event1 = Event(
            title="Semana Acadêmica de Tecnologia",
            description="Palestras e workshops sobre IA e Desenvolvimento de Software.",
            event_date=datetime.now() + timedelta(days=15)
        )
        db.add(event1)
        
        await db.commit()
        print("🚀 Seed finalizado com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed())