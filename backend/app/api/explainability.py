from fastapi import APIRouter, Depends

from app.schemas.prediction import CardiovascularPredictionRequest
from app.security.dependencies import get_current_user
from ml.explainability.shap_explainer import CardiovascularSHAPExplainer


router = APIRouter(
    prefix="/explainability",
    tags=["Explainability"],
)

explainer = CardiovascularSHAPExplainer(
    "ml/models/artifacts/"
    "cardiovascular_logistic_regression.joblib"
)


@router.post("/cardiovascular-risk")
async def explain_cardiovascular_risk(
    request: CardiovascularPredictionRequest,
    current_user: dict = Depends(get_current_user),
):
    return {
        "explanation": explainer.explain(
            request.model_dump()
        ),
        "disclaimer": (
            "SHAP explanation describes model behavior. "
            "It does not establish clinical causality."
        ),
    }
