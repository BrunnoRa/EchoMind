from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.core.database import Base
import uuid

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String, nullable=False, default="Geral")
    # Ajustado para 1024 para ser compatível com mxbai-embed-large
    embedding = Column(Vector(1024)) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())