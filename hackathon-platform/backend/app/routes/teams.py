from fastapi import APIRouter, Depends, HTTPException, Header
from app.database import get_db
from app.schemas.team import TeamCreate, TeamMemberAdd, Team
from typing import List, Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from typing import List

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

@router.get("/event/{event_id}")
async def get_event_teams(event_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, COUNT(tm.user_id) as member_count
        FROM teams t
        LEFT JOIN team_members tm ON t.team_id = tm.team_id
        WHERE t.event_id = %s
        GROUP BY t.team_id
        ORDER BY t.created_date DESC
    """, (event_id,))
    teams = cursor.fetchall()
    cursor.close()
    return teams

@router.get("/{team_id}")
async def get_team(team_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT t.*, COUNT(tm.user_id) as member_count
        FROM teams t
        LEFT JOIN team_members tm ON t.team_id = tm.team_id
        WHERE t.team_id = %s
        GROUP BY t.team_id
    """, (team_id,))
    team = cursor.fetchone()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Get members
    cursor.execute("""
        SELECT u.user_id, u.email, u.full_name, tm.joined_date
        FROM team_members tm
        JOIN users u ON tm.user_id = u.user_id
        WHERE tm.team_id = %s
    """, (team_id,))
    members = cursor.fetchall()
    team["members"] = members
    
    cursor.close()
    return team

@router.post("/", response_model=Team)
async def create_team(team: TeamCreate, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    cursor.execute(
        "INSERT INTO teams (name, event_id, leader_id, description) VALUES (%s, %s, %s, %s)",
        (team.name, team.event_id, user_id, team.description)
    )
    db.commit()
    team_id = cursor.lastrowid
    
    # Add leader as member
    cursor.execute(
        "INSERT INTO team_members (team_id, user_id) VALUES (%s, %s)",
        (team_id, user_id)
    )
    db.commit()
    
    cursor.execute("""
        SELECT t.*, COUNT(tm.user_id) as member_count
        FROM teams t
        LEFT JOIN team_members tm ON t.team_id = tm.team_id
        WHERE t.team_id = %s
        GROUP BY t.team_id
    """, (team_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@router.post("/{team_id}/members")
async def add_team_member(team_id: int, member: TeamMemberAdd, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    # Verify user is team leader
    cursor.execute("SELECT leader_id FROM teams WHERE team_id = %s", (team_id,))
    team = cursor.fetchone()
    if not team or team["leader_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Add member
    try:
        cursor.execute(
            "INSERT INTO team_members (team_id, user_id) VALUES (%s, %s)",
            (team_id, member.user_id)
        )
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Member already in team")
    
    cursor.close()
    return {"message": "Member added successfully"}

@router.delete("/{team_id}/members/{member_id}")
async def remove_team_member(team_id: int, member_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    # Verify user is team leader
    cursor.execute("SELECT leader_id FROM teams WHERE team_id = %s", (team_id,))
    team = cursor.fetchone()
    if not team or team["leader_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    cursor.execute(
        "DELETE FROM team_members WHERE team_id = %s AND user_id = %s",
        (team_id, member_id)
    )
    db.commit()
    cursor.close()
    return {"message": "Member removed successfully"}
