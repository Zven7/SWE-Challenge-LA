from datetime import datetime
from typing import Optional

from bson import ObjectId
from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from ..db.models.user import UserRole


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    active: bool = True


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: Optional[str] = Field(default=None, min_length=1)
    last_name: Optional[str] = Field(default=None, min_length=1)
    role: Optional[UserRole] = None
    active: Optional[bool] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    active: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("id", mode="before")
    def convert_id(cls, value):
        if isinstance(value, (ObjectId, PydanticObjectId)):
            return str(value)
        return value

class UserListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    limit: int
    skip: int
    items: list[UserResponse]