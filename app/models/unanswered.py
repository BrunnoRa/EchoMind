import uuid
from sqlalchemy import Column, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.core.database import Base

# CORRIGIDO: era 1536 (OpenAI), agora 1024 para ser compatível com mxbai-embed-large (Ollama)
EMBEDDING_DIM = 1024


class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM))
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
