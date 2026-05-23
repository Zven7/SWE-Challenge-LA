from typing import Optional

from fastapi import APIRouter, Query, status

from app.schemas.user import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService
from app.utils.pagination import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: UserCreate):
    return await UserService.create_user(payload)


@router.get("", response_model=UserListResponse)
async def get_users(
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    skip: int = Query(DEFAULT_SKIP, ge=0),
    role: Optional[str] = None,
    active: Optional[bool] = None,
):
    return await UserService.get_users(
        limit=limit,
        skip=skip,
        role=role,
        active=active,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    return await UserService.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    payload: UserUpdate,
):
    return await UserService.update_user(user_id, payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: str):
    await UserService.delete_user(user_id)