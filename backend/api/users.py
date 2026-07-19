from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    get_password_hash,
    verify_password,
)
from backend.database.database import get_db
from backend.database.models import User, UserSettings
from backend.schemas.user import RefreshTokenRequest, TokenResponse, UserCreate, UserLogin, UserRead

router = APIRouter()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, payload: UserCreate) -> User:
    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    settings_record = UserSettings(user_id=user.id)
    db.add(settings_record)
    db.commit()
    db.refresh(settings_record)

    return user


@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return create_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id, "role": user.role})
    refresh_token = create_refresh_token({"user_id": user.id, "role": user.role})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest) -> TokenResponse:
    token = payload.refresh_token
    payload_data = decode_jwt_token(token)
    if payload_data is None or "user_id" not in payload_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = create_access_token({"user_id": payload_data["user_id"], "role": payload_data.get("role", "user")})
    refresh_token_value = create_refresh_token({"user_id": payload_data["user_id"], "role": payload_data.get("role", "user")})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token_value)
