from fastapi import APIRouter, Depends

from app.schemas.patient import (
    AllergyCreate,
    ChronicConditionCreate,
    ClinicalNoteCreate,
    DiagnosisCreate,
    MedicalEventCreate,
    MedicalHistoryCreate,
    MedicationCreate,
    PatientCreate,
)
from app.security.dependencies import get_current_user
from app.services.patient import (
    add_patient_data,
    create_patient,
    get_patient_for_user,
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


def serialize_patient(patient: dict) -> dict:
    return {
        "id": str(patient["_id"]),
        "user_id": str(patient["user_id"]),
        "date_of_birth": patient.get("date_of_birth"),
        "gender": patient.get("gender"),
        "blood_type": patient.get("blood_type"),
        "created_at": patient["created_at"],
        "updated_at": patient["updated_at"],
    }


@router.post("")
async def create_my_patient_profile(
    data: PatientCreate,
    current_user=Depends(get_current_user),
):
    patient = await create_patient(
        str(current_user["_id"]),
        data,
    )

    return serialize_patient(patient)


@router.get("/me")
async def get_my_patient_profile(
    current_user=Depends(get_current_user),
):
    patient = await get_patient_for_user(
        str(current_user["_id"])
    )

    return serialize_patient(patient)


@router.post("/me/medical-history")
async def add_medical_history(
    data: MedicalHistoryCreate,
    current_user=Depends(get_current_user),
):
    patient = await add_patient_data(
        str(current_user["_id"]),
        "medical_history",
        data.model_dump(),
    )

    return patient["medical_history"][-1]


@router.post("/me/allergies")
async def add_allergy(
    data: AllergyCreate,
    current_user=Depends(get_current_user),
):
    patient = await add_patient_data(
        str(current_user["_id"]),
        "allergies",
        data.model_dump(),
    )

    return patient["allergies"][-1]


@router.post("/me/chronic-conditions")
async def add_chronic_condition(
    data: ChronicConditionCreate,
    current_user=Depends(get_current_user),
):
    patient = await add_patient_data(
        str(current_user["_id"]),
        "chronic_conditions",
        data.model_dump(),
    )

    return patient["chronic_conditions"][-1]


@router.post("/me/diagnoses")
async def add_diagnosis(
    data: DiagnosisCreate,
    current_user=Depends(get_current_user),
):
    patient = await add_patient_data(
        str(current_user["_id"]),
        "diagnoses",
        data.model_dump(),
    )

    return patient["diagnoses"][-1]


@router.post("/me/medications")
async def add_medication(
    data: MedicationCreate,
    current_user=Depends(get_current_user),
):
    patient = await add_patient_data(
        str(current_user["_id"]),
        "medications",
        data.model_dump(),
    )

    return patient["medications"][-1]


@router.post("/me/clinical-notes")
async def add_clinical_note(
    data: ClinicalNoteCreate,
    current_user=Depends(get_current_user),
):
    patient = await add_patient_data(
        str(current_user["_id"]),
        "clinical_notes",
        data.model_dump(),
    )

    return patient["clinical_notes"][-1]


@router.post("/me/medical-events")
async def add_medical_event(
    data: MedicalEventCreate,
    current_user=Depends(get_current_user),
):
    patient = await add_patient_data(
        str(current_user["_id"]),
        "medical_events",
        data.model_dump(),
    )

    return patient["medical_events"][-1]
