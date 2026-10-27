from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoDB:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongodb = MongoDB()


async def connect_to_mongodb() -> None:
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)

    await mongodb.client.admin.command("ping")

    mongodb.database = mongodb.client[settings.MONGODB_DATABASE]

    print("MongoDB connected successfully")


async def close_mongodb_connection() -> None:
    if mongodb.client:
        mongodb.client.close()
        print("MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    if mongodb.database is None:
        raise RuntimeError("MongoDB is not initialized")

    return mongodb.database


async def create_database_indexes() -> None:
    if mongodb.database is None:
        raise RuntimeError("MongoDB is not initialized")

    await mongodb.database.users.create_index(
        "email",
        unique=True,
    )


async def create_patient_indexes() -> None:
    if mongodb.database is None:
        raise RuntimeError("MongoDB is not initialized")

    await mongodb.database.patients.create_index(
        "user_id",
        unique=True,
    )


async def create_prediction_indexes() -> None:
    if mongodb.database is None:
        raise RuntimeError("MongoDB is not initialized")

    await mongodb.database.predictions.create_index(
        [("patient_id", 1), ("created_at", -1)]
    )
