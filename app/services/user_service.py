from datetime import datetime, timezone
from typing import Optional

from beanie import PydanticObjectId
from bson.errors import InvalidId

from ..core.exceptions import (
    DuplicateUserException,
    UserNotFoundException,
)
from ..db.models.user import User
from ..schemas.user import UserCreate, UserUpdate

class UserService:
    @staticmethod
    async def create_user(payload: UserCreate) -> User:
        existing_username = await User.find_one(
            User.username == payload.username
        )

        if existing_username:
            raise DuplicateUserException("username")

        existing_email = await User.find_one(
            User.email == payload.email
        )

        if existing_email:
            raise DuplicateUserException("email")

        user = User(**payload.model_dump())

        await user.insert()

        return user

    @staticmethod
    async def get_users(
        limit: int,
        skip: int,
        role: Optional[str] = None,
        active: Optional[bool] = None,
    ):
        filters = {}

        if role:
            filters["role"] = role

        if active is not None:
            filters["active"] = active

        total = await User.find(filters).count()

        users = (
            await User.find(filters)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return {
            "total": total,
            "limit": limit,
            "skip": skip,
            "items": users,
        }
    
    @staticmethod
    async def get_user(user_id: str) -> User:
        try:
            object_id = PydanticObjectId(user_id)
        except (ValueError, InvalidId):
            raise UserNotFoundException()

        user = await User.get(object_id)

        if not user:
            raise UserNotFoundException()

        return user
    
    
    @staticmethod
    async def update_user(
        user_id: str,
        payload: UserUpdate,
    ) -> User:
        try:
            object_id = PydanticObjectId(user_id)
        except (ValueError, InvalidId):
            raise UserNotFoundException()

        user = await User.get(object_id)

        if not user:
            raise UserNotFoundException()

        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)

        await user.save()

        return user
    
    @staticmethod
    async def delete_user(user_id: str):
        try:
            object_id = PydanticObjectId(user_id)
        except (ValueError, InvalidId):
            raise UserNotFoundException()

        user = await User.get(object_id)

        if not user:
            raise UserNotFoundException()

        await user.delete()