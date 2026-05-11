from fastapi import APIRouter, Depends, HTTPException, Header
from app.database import get_db
from app.schemas.registration import RegistrationCreate, Registration
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

@router.get("/my")
async def get_my_registrations(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, e.title as event_title, e.status as event_status, e.start_date, e.end_date
        FROM registrations r
        JOIN events e ON r.event_id = e.event_id
        WHERE r.user_id = %s
        ORDER BY r.registered_date DESC
    """, (user_id,))
    registrations = cursor.fetchall()
    cursor.close()
    return registrations

@router.post("/", response_model=Registration)
async def register_event(registration: RegistrationCreate, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    # Check if already registered
    cursor.execute(
        "SELECT * FROM registrations WHERE user_id = %s AND event_id = %s",
        (user_id, registration.event_id)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Already registered for this event")
    
    # Create registration
    cursor.execute(
        "INSERT INTO registrations (user_id, event_id, status) VALUES (%s, %s, %s)",
        (user_id, registration.event_id, "confirmed")
    )
    db.commit()
    registration_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM registrations WHERE registration_id = %s", (registration_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@router.delete("/{registration_id}")
async def cancel_registration(registration_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    # Verify ownership
    cursor.execute(
        "SELECT * FROM registrations WHERE registration_id = %s AND user_id = %s",
        (registration_id, user_id)
    )
    if not cursor.fetchone():
        raise HTTPException(status_code=403, detail="Not authorized")
    
    cursor.execute("DELETE FROM registrations WHERE registration_id = %s", (registration_id,))
    db.commit()
    cursor.close()
    return {"message": "Registration cancelled"}

@router.get("/")
async def get_all_registrations(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, u.email, u.full_name, e.title as event_title
        FROM registrations r
        JOIN users u ON r.user_id = u.user_id
        JOIN events e ON r.event_id = e.event_id
        ORDER BY r.registered_date DESC
    """)
    registrations = cursor.fetchall()
    cursor.close()
    return registrations
