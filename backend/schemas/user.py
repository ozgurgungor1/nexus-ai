from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    role: str
    is_active: bool

    class Config:
        orm_mode = True
