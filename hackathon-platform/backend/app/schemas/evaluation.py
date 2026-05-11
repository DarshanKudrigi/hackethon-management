from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EvaluationCreate(BaseModel):
    project_id: int
    score: int
    feedback: Optional[str] = None

class Evaluation(BaseModel):
    evaluation_id: int
    project_id: int
    judge_id: int
    score: int
    feedback: Optional[str] = None
    evaluated_date: datetime

    class Config:
        from_attributes = True
