from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TeamCreate(BaseModel):
    name: str
    event_id: int
    description: Optional[str] = None

class TeamMemberAdd(BaseModel):
    user_id: int

class Team(BaseModel):
    team_id: int
    name: str
    event_id: int
    leader_id: int
    description: Optional[str] = None
    created_date: datetime
    member_count: Optional[int] = 0

    class Config:
        from_attributes = True
