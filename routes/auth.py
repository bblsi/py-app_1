from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import uuid
import time
from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional

SECRET_KEY = "root123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

active_sessions = {}

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_current_user(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})

    session = active_sessions.get(token)
    if not session:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})

    if time.time() - session["timestamp"] > 120:
        del active_sessions[token]
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})

    session["timestamp"] = time.time()
    return session["user"]

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret":
        token = str(uuid.uuid4())
        user_data = {
            "username": username,
            "login_time": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        }
        active_sessions[token] = {
            "user": user_data,
            "timestamp": time.time()
        }

        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=120
        )
        return response

    raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})

@router.get("/user")
async def get_user_profile(current_user=Depends(get_current_user)):
    from routes.movie import movies

    return {
        "profile": current_user,
        "movies": movies
    }

def create_access_token(  data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login-jwt")
async def login_jwt(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret":
        token_data = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
        access_token = create_access_token(data=token_data)
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})

def verify_jwt_token(token: str) -> str:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail={"message": "Invalid token"})
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail={"message": "Token expired"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail={"message": "Invalid token"})