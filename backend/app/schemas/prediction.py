from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CardiovascularPredictionRequest(BaseModel):
    age: float = Field(..., ge=18, le=120)
    sex: int = Field(..., ge=0, le=1)
    cp: int = Field(..., ge=0, le=3)
    trestbps: float = Field(..., gt=0)
    chol: float = Field(..., gt=0)
    fbs: int = Field(..., ge=0, le=1)
    restecg: int = Field(..., ge=0, le=2)
    thalach: float = Field(..., gt=0)
    exang: int = Field(..., ge=0, le=1)
    oldpeak: float = Field(..., ge=0)
    slope: int = Field(..., ge=0, le=2)
    ca: int = Field(..., ge=0, le=3)
    thal: int = Field(..., ge=0, le=3)


class CardiovascularPredictionResponse(BaseModel):
    probability: float
    risk_score: float
    risk_category: str
    model: str
    disclaimer: str


class PredictionHistoryItem(BaseModel):
    id: str
    patient_id: str
    probability: float
    risk_score: float
    risk_category: str
    model: str
    input_features: dict[str, Any]
    created_at: datetime
