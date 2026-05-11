from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str = "upcoming"

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None

class Event(EventCreate):
    event_id: int

    class Config:
        from_attributes = True
