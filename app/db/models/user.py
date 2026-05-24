from datetime import datetime, timezone
from enum import Enum

from beanie import Document
from pydantic import EmailStr, Field


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class User(Document):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    class Settings:
        name = "users"
        indexes = [
            "username",
            "email",
        ]