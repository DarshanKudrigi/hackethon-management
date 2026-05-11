from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: str
    github_url: Optional[str] = None
    team_id: int

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    github_url: Optional[str] = None
    status: Optional[str] = None

class Project(BaseModel):
    project_id: int
    title: str
    description: str
    github_url: Optional[str] = None
    team_id: int
    event_id: int
    status: str
    created_date: datetime

    class Config:
        from_attributes = True
