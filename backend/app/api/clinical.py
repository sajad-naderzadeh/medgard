from fastapi import APIRouter, Depends

from app.schemas.clinical import (
    ClinicalObservationCreate,
    LabResultCreate,
    MedicalDocumentCreate,
    PrescriptionCreate,
    VitalSignsCreate,
)
from app.security.dependencies import get_current_user
from app.services.clinical import (
    add_lab_result,
    add_observation,
    add_prescription,
    add_vital_signs,
    get_clinical_records,
)


router = APIRouter(
    prefix="/clinical",
    tags=["Clinical Data"],
)


@router.post("/vital-signs")
async def create_vital_signs(
    data: VitalSignsCreate,
    current_user=Depends(get_current_user),
):
    await add_vital_signs(
        str(current_user["_id"]),
        data,
    )

    return {
        "message": "Vital signs recorded successfully"
    }


@router.get("/vital-signs")
async def get_vital_signs(
    current_user=Depends(get_current_user),
):
    return await get_clinical_records(
        str(current_user["_id"]),
        "vital_signs",
    )


@router.post("/lab-results")
async def create_lab_result(
    data: LabResultCreate,
    current_user=Depends(get_current_user),
):
    await add_lab_result(
        str(current_user["_id"]),
        data,
    )

    return {
        "message": "Lab result recorded successfully"
    }


@router.get("/lab-results")
async def get_lab_results(
    current_user=Depends(get_current_user),
):
    return await get_clinical_records(
        str(current_user["_id"]),
        "lab_results",
    )


@router.post("/observations")
async def create_observation(
    data: ClinicalObservationCreate,
    current_user=Depends(get_current_user),
):
    await add_observation(
        str(current_user["_id"]),
        data,
    )

    return {
        "message": "Clinical observation recorded successfully"
    }


@router.get("/observations")
async def get_observations(
    current_user=Depends(get_current_user),
):
    return await get_clinical_records(
        str(current_user["_id"]),
        "clinical_observations",
    )


@router.post("/prescriptions")
async def create_prescription(
    data: PrescriptionCreate,
    current_user=Depends(get_current_user),
):
    await add_prescription(
        str(current_user["_id"]),
        data,
    )

    return {
        "message": "Prescription recorded successfully"
    }


@router.get("/prescriptions")
async def get_prescriptions(
    current_user=Depends(get_current_user),
):
    return await get_clinical_records(
        str(current_user["_id"]),
        "prescriptions",
    )
