from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None

class FAQResponse(FAQBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)