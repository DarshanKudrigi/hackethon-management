from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas.event import EventCreate, EventUpdate, Event
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Event])
async def get_events(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events ORDER BY start_date DESC")
    events = cursor.fetchall()
    cursor.close()
    return events

@router.get("/{event_id}", response_model=Event)
async def get_event(event_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    event = cursor.fetchone()
    cursor.close()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/", response_model=Event)
async def create_event(event: EventCreate, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO events (title, description, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)",
        (event.title, event.description, event.start_date, event.end_date, event.status)
    )
    db.commit()
    event_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@router.put("/{event_id}", response_model=Event)
async def update_event(event_id: int, event: EventUpdate, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    update_fields = []
    update_values = []
    
    if event.title:
        update_fields.append("title = %s")
        update_values.append(event.title)
    if event.description:
        update_fields.append("description = %s")
        update_values.append(event.description)
    if event.start_date:
        update_fields.append("start_date = %s")
        update_values.append(event.start_date)
    if event.end_date:
        update_fields.append("end_date = %s")
        update_values.append(event.end_date)
    if event.status:
        update_fields.append("status = %s")
        update_values.append(event.status)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_values.append(event_id)
    query = f"UPDATE events SET {', '.join(update_fields)} WHERE event_id = %s"
    cursor.execute(query, update_values)
    db.commit()
    
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@router.delete("/{event_id}")
async def delete_event(event_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))
    db.commit()
    cursor.close()
    return {"message": "Event deleted successfully"}
