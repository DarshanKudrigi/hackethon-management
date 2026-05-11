from fastapi import APIRouter, Depends, HTTPException, Header
from app.database import get_db
from app.schemas.evaluation import EvaluationCreate, Evaluation
from typing import List, Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Security config
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(authorization: Optional[str] = Header(None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/project/{project_id}")
async def get_project_evaluations(project_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.full_name as judge_name
        FROM evaluations e
        JOIN users u ON e.judge_id = u.user_id
        WHERE e.project_id = %s
        ORDER BY e.evaluated_date DESC
    """, (project_id,))
    evaluations = cursor.fetchall()
    cursor.close()
    return evaluations

@router.post("/", response_model=Evaluation)
async def create_evaluation(evaluation: EvaluationCreate, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    # Verify score is valid
    if evaluation.score < 0 or evaluation.score > 100:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")
    
    cursor.execute(
        "INSERT INTO evaluations (project_id, judge_id, score, feedback) VALUES (%s, %s, %s, %s)",
        (evaluation.project_id, user_id, evaluation.score, evaluation.feedback)
    )
    db.commit()
    evaluation_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM evaluations WHERE evaluation_id = %s", (evaluation_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@router.get("/")
async def get_all_evaluations(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, u.full_name as judge_name, p.title as project_title
        FROM evaluations e
        JOIN users u ON e.judge_id = u.user_id
        JOIN projects p ON e.project_id = p.project_id
        ORDER BY e.evaluated_date DESC
    """)
    evaluations = cursor.fetchall()
    cursor.close()
    return evaluations
