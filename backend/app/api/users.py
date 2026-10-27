from fastapi import APIRouter, Depends

from app.security.dependencies import (
    get_current_user,
    require_roles,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
async def get_my_profile(
    current_user=Depends(get_current_user),
):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "role": current_user["role"],
        "first_name": current_user["first_name"],
        "last_name": current_user["last_name"],
        "is_active": current_user["is_active"],
    }


@router.get("/admin")
async def admin_endpoint(
    current_user=Depends(
        require_roles("admin")
    ),
):
    return {
        "message": "Admin access granted",
        "user_id": str(current_user["_id"]),
    }


@router.get("/doctors")
async def doctor_endpoint(
    current_user=Depends(
        require_roles("doctor", "admin")
    ),
):
    return {
        "message": "Doctor access granted",
        "user_id": str(current_user["_id"]),
        "role": current_user["role"],
    }
