from fastapi import APIRouter, status

from app.schemas.user import (
    TokenResponse,
    UserLogin,
    UserRegister,
)
from app.services.auth import (
    authenticate_user,
    register_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(data: UserRegister):
    user = await register_user(data)

    return {
        "message": "User registered successfully",
        "user_id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"],
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(data: UserLogin):
    result = await authenticate_user(
        email=data.email,
        password=data.password,
    )

    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
    }
