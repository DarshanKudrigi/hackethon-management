from fastapi import APIRouter, Depends, HTTPException, Header
from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate, Project
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

@router.get("/")
async def get_projects(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, COUNT(e.evaluation_id) as evaluation_count, AVG(e.score) as avg_score
        FROM projects p
        LEFT JOIN evaluations e ON p.project_id = e.project_id
        GROUP BY p.project_id
        ORDER BY p.created_date DESC
    """)
    projects = cursor.fetchall()
    cursor.close()
    return projects

@router.get("/{project_id}")
async def get_project(project_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, COUNT(e.evaluation_id) as evaluation_count, AVG(e.score) as avg_score
        FROM projects p
        LEFT JOIN evaluations e ON p.project_id = e.project_id
        WHERE p.project_id = %s
        GROUP BY p.project_id
    """, (project_id,))
    project = cursor.fetchone()
    cursor.close()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    # Get event_id from team
    cursor.execute("SELECT event_id FROM teams WHERE team_id = %s", (project.team_id,))
    team = cursor.fetchone()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    cursor.execute(
        "INSERT INTO projects (title, description, github_url, team_id, event_id, status) VALUES (%s, %s, %s, %s, %s, %s)",
        (project.title, project.description, project.github_url, project.team_id, team["event_id"], "submitted")
    )
    db.commit()
    project_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: int, project: ProjectUpdate, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    update_fields = []
    update_values = []
    
    if project.title:
        update_fields.append("title = %s")
        update_values.append(project.title)
    if project.description:
        update_fields.append("description = %s")
        update_values.append(project.description)
    if project.github_url:
        update_fields.append("github_url = %s")
        update_values.append(project.github_url)
    if project.status:
        update_fields.append("status = %s")
        update_values.append(project.status)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_values.append(project_id)
    query = f"UPDATE projects SET {', '.join(update_fields)} WHERE project_id = %s"
    cursor.execute(query, update_values)
    db.commit()
    
    cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@router.delete("/{project_id}")
async def delete_project(project_id: int, user_id: int = None, db=Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
    db.commit()
    cursor.close()
    return {"message": "Project deleted successfully"}
