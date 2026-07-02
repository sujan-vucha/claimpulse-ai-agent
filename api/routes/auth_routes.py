"""
auth_routes.py

Authentication endpoints for registration, login, and profile fetching.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import Token, UserAuth, verify_password, get_password_hash, create_access_token, get_current_user
from api.db import db_manager

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
async def register(user: UserAuth):
    existing = db_manager.get_user(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pwd = get_password_hash(user.password)
    user_doc = {
        "username": user.username,
        "password_hash": hashed_pwd,
        "role": user.role or "policyholder",
        "full_name": user.full_name or user.username.split("@")[0].capitalize()
    }
    db_manager.create_user(user_doc)
    
    access_token = create_access_token(data={"sub": user.username, "role": user_doc["role"]})
    safe_user = {k: v for k, v in user_doc.items() if k != "password_hash"}
    return {"access_token": access_token, "token_type": "bearer", "user": safe_user}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_manager.get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"], "role": user.get("role", "policyholder")})
    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    return {"access_token": access_token, "token_type": "bearer", "user": safe_user}

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
