from fastapi import APIRouter, Depends, HTTPException

from app.schemas.prediction import (
    CardiovascularPredictionRequest,
    CardiovascularPredictionResponse,
    PredictionHistoryItem,
)
from app.services.prediction import CardiovascularPredictionService
from app.security.dependencies import get_current_user


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)

prediction_service = CardiovascularPredictionService()


@router.post(
    "/cardiovascular-risk",
    response_model=CardiovascularPredictionResponse,
)
async def predict_cardiovascular_risk(
    request: CardiovascularPredictionRequest,
    current_user: dict = Depends(get_current_user),
):
    patient_id = str(
        current_user.get("patient_id")
        or current_user.get("_id")
        or current_user.get("id")
    )

    return await prediction_service.predict(
        request.model_dump(),
        patient_id=patient_id,
    )


@router.get(
    "/me",
    response_model=list[PredictionHistoryItem],
)
async def get_prediction_history(
    current_user: dict = Depends(get_current_user),
):
    patient_id = str(
        current_user.get("patient_id")
        or current_user.get("_id")
        or current_user.get("id")
    )

    records = await prediction_service.history(patient_id)

    return [
        {
            "id": record["_id"],
            "patient_id": record["patient_id"],
            "probability": record["probability"],
            "risk_score": record["risk_score"],
            "risk_category": record["risk_category"],
            "model": record["model"],
            "input_features": record["input_features"],
            "created_at": record["created_at"],
        }
        for record in records
    ]
