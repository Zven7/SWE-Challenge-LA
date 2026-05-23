from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.db.models.user import UserRole


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    active: bool = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1)
    last_name: Optional[str] = Field(default=None, min_length=1)
    role: Optional[UserRole] = None
    active: Optional[bool] = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    active: bool
    created_at: datetime
    updated_at: datetime

class UserListResponse(BaseModel):
    total: int
    limit: int
    skip: int
    items: list[UserResponse]