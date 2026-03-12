from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def init_db():
    """
    Inicializa o banco de dados:
    1. Habilita a extensão pgvector
    2. Importa todos os modelos para que o SQLAlchemy os registre no Base.metadata
    3. Cria todas as tabelas
    """
    # CRÍTICO: importar todos os modelos ANTES do create_all
    # Sem isso, o Base.metadata não sabe que as tabelas existem
    from app.models import admin, faq, document, event, interaction, unanswered  # noqa: F401

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
