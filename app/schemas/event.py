from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: str | None = None
    event_date: datetime

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    