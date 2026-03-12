import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.core.database import Base

# mxbai-embed-large gera vetores de 1024 dimensões
EMBEDDING_DIM = 1024


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String, nullable=False, default="Geral")
    is_active = Column(Boolean, nullable=False, default=True)
    embedding = Column(Vector(EMBEDDING_DIM))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
