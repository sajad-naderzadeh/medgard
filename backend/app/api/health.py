from fastapi import APIRouter

from app.core.database import get_database


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check():
    db = get_database()

    await db.command("ping")

    return {
        "status": "healthy",
        "service": "medguard-ai",
        "database": "connected",
    }
