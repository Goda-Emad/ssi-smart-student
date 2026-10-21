"""
SSI — Auth Router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from schemas.auth import LoginRequest, TokenResponse
from utils.security import create_access_token, decode_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Demo users (in production, store in DB with hashed passwords)
DEMO_USERS = {
    "student": {"password": "student123", "role": "student", "student_id": "STU00001"},
    "advisor": {"password": "advisor123", "role": "advisor", "student_id": None},
    "admin":   {"password": "admin123",   "role": "admin",   "student_id": None},
}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = DEMO_USERS.get(payload.username)
    if not user or user["password"] != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(
        data={
            "sub": payload.username,
            "role": user["role"],
            "student_id": user["student_id"],
        }
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        role=user["role"],
        student_id=user["student_id"],
    )


@router.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    data = decode_access_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return data
