from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, User, TokenResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (email, full_name, password, role) VALUES (%s, %s, %s, %s)",
        (user.email, user.full_name, hashed_password, user.role)
    )
    db.commit()
    
    # Get created user
    cursor.execute("SELECT user_id, email, full_name, role FROM users WHERE email = %s", (user.email,))
    user_data = cursor.fetchone()
    cursor.close()
    
    # Create token
    access_token = create_access_token({"sub": user.email, "user_id": user_data["user_id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": User(**user_data)
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (credentials.email,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user["email"], "user_id": user["user_id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": User(
            user_id=user["user_id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"]
        )
    }

def get_current_user(token: str = None, db=None):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_id

@router.get("/me", response_model=User)
async def get_profile(authorization: str = None, db=Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id, email, full_name, role FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user)
