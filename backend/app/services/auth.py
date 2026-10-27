from fastapi import HTTPException, status

from app.core.database import get_database
from app.models.user import UserModel, UserRole
from app.schemas.user import UserRegister
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password


async def register_user(data: UserRegister) -> dict:
    db = get_database()

    existing_user = await db.users.find_one(
        {"email": data.email.lower().strip()}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    user = UserModel.create_document(
        email=data.email,
        hashed_password=hash_password(data.password),
        role=UserRole.PATIENT,
        first_name=data.first_name,
        last_name=data.last_name,
    )

    await db.users.insert_one(user)

    return user


async def authenticate_user(
    email: str,
    password: str,
) -> dict:
    db = get_database()

    user = await db.users.find_one(
        {"email": email.lower().strip()}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        password,
        user["hashed_password"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    token = create_access_token(
        subject=str(user["_id"]),
        role=user["role"],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }
