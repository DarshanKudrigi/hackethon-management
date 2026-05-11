from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegistrationCreate(BaseModel):
    event_id: int

class Registration(BaseModel):
    registration_id: int
    user_id: int
    event_id: int
    status: str
    registered_date: datetime

    class Config:
        from_attributes = True
