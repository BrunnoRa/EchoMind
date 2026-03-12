"""
Script de seed para popular o banco de dados com dados iniciais.

Como rodar (dentro do container):
    docker exec -it totem_api python seed.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import AsyncSessionLocal, init_db
from app.services.faq_service import FAQService
from app.services.auth_service import AuthService
from app.schemas.faq import FAQCreate
from app.schemas.admin import AdminCreate
from app.models.event import Event
from datetime import datetime, timedelta


FAQS_INICIAIS = [
    FAQCreate(question="Onde fica a secretaria?", answer="A secretaria central fica no Bloco A, térreo, funcionando de segunda a sexta das 08h às 22h.", category="Localização"),
    FAQCreate(question="Como emitir o histórico escolar?", answer="Você pode emitir o histórico escolar pelo portal do aluno na aba 'Documentos', ou solicitar presencialmente na secretaria com documento de identificação.", category="Documentos"),
    FAQCreate(question="Quais são as regras da biblioteca?", answer="A biblioteca permite empréstimo de até 3 livros por 7 dias corridos. O atraso gera multa de R$ 2,00 por dia por livro. Renovações podem ser feitas pelo portal do aluno.", category="Biblioteca"),
    FAQCreate(question="Qual o horário do Restaurante Universitário?", answer="O RU funciona de segunda a sexta. Café da manhã: 07h às 09h. Almoço: 11h às 14h. Jantar: 17h30 às 19h30.", category="RU"),
    FAQCreate(question="Como trancar uma disciplina?", answer="O trancamento de disciplinas pode ser feito pelo portal do aluno durante o período de ajuste, que ocorre nas duas primeiras semanas do semestre.", category="Acadêmico"),
    FAQCreate(question="Onde fica o laboratório de informática?", answer="Os laboratórios de informática ficam no Bloco C, salas 201, 202 e 203, no segundo andar. Funcionam de segunda a sexta das 07h às 22h.", category="Localização"),
    FAQCreate(question="Como solicitar segunda via do cartão estudantil?", answer="Para solicitar segunda via do cartão estudantil, dirija-se à secretaria com documento de identidade e comprovante de matrícula. O prazo de emissão é de 5 dias úteis.", category="Documentos"),
    FAQCreate(question="Qual é o calendário acadêmico?", answer="O calendário acadêmico está disponível no portal do aluno e no site da universidade. Você também pode solicitar uma cópia impressa na secretaria.", category="Acadêmico"),
]


async def seed():
    print("🌱 Iniciando seed do banco de dados EchoMind...\n")

    print("📦 Verificando/criando tabelas...")
    await init_db()
    print("✅ Tabelas prontas.\n")

    # ── 1. Admin (sessão própria) ─────────────────────────────────────────────
    print("👤 Criando admin padrão...")
    async with AsyncSessionLocal() as db:
        try:
            admin = await AuthService.register_admin(db, AdminCreate(username="admin", password="admin123"))
            print(f"✅ Admin criado: {admin.username} (senha: admin123)\n")
        except Exception as e:
            await db.rollback()
            print(f"⚠️  Admin já existe, pulando.\n")

    # ── 2. FAQs — cada um em sessão própria ──────────────────────────────────
    print("📚 Inserindo FAQs com embeddings (isso pode levar um momento)...")
    for faq_in in FAQS_INICIAIS:
        async with AsyncSessionLocal() as db:
            try:
                faq = await FAQService.create_faq(db, faq_in)
                print(f"  ✅ [{faq.category}] {faq.question[:60]}")
            except Exception as e:
                await db.rollback()
                print(f"  ❌ Erro ao criar FAQ '{faq_in.question[:40]}': {e}")

    # ── 3. Eventos (sessão própria) ───────────────────────────────────────────
    print("\n📅 Inserindo eventos de exemplo...")
    events = [
        Event(title="Semana Acadêmica de Tecnologia", description="Palestras e workshops sobre IA, Cloud e Desenvolvimento de Software.", event_date=datetime.now() + timedelta(days=15), event_type="palestra"),
        Event(title="Feira de Estágios e Empregos", description="Mais de 50 empresas presentes. Traga seu currículo impresso.", event_date=datetime.now() + timedelta(days=30), event_type="evento_social"),
        Event(title="Defesa de TCCs - Engenharia de Software", description="Apresentações abertas ao público no Auditório Principal, Bloco B.", event_date=datetime.now() + timedelta(days=7), event_type="outro"),
    ]

    async with AsyncSessionLocal() as db:
        try:
            for event in events:
                db.add(event)
            await db.commit()
            for event in events:
                print(f"  ✅ Evento: {event.title}")
        except Exception as e:
            await db.rollback()
            print(f"  ❌ Erro ao inserir eventos: {e}")

    print("\n🚀 Seed finalizado!")
    print("   Acesse a documentação em: http://localhost:8000/docs")


if __name__ == "__main__":
    asyncio.run(seed())