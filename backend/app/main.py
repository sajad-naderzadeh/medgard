from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.patients import router as patients_router
from app.api.clinical import router as clinical_router
from app.api.predictions import router as predictions_router
from app.api.explainability import router as explainability_router
from app.core.config import settings, validate_production_settings
from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
    create_database_indexes,
    create_patient_indexes,
    create_prediction_indexes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_production_settings()
    await connect_to_mongodb()
    await create_database_indexes()
    await create_patient_indexes()
    await create_prediction_indexes()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade AI for Health platform",
    lifespan=lifespan,
)


app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(patients_router, prefix="/api/v1")
app.include_router(clinical_router, prefix="/api/v1")
app.include_router(predictions_router, prefix="/api/v1")
app.include_router(explainability_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }
