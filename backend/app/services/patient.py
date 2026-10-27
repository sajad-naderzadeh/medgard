from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.patient import PatientModel
from app.repositories.patient import PatientRepository


async def create_patient(user_id: str, data):
    existing = await PatientRepository.find_by_user_id(user_id)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Patient profile already exists",
        )

    document = PatientModel.create_document(
        user_id=user_id,
        date_of_birth=data.date_of_birth,
        gender=data.gender,
        blood_type=data.blood_type,
    )

    return await PatientRepository.create(document)


async def get_patient_for_user(user_id: str):
    patient = await PatientRepository.find_by_user_id(user_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found",
        )

    return patient


async def add_patient_data(
    user_id: str,
    field: str,
    data: dict,
):
    patient = await get_patient_for_user(user_id)

    data["created_at"] = datetime.now(timezone.utc)

    return await PatientRepository.push(
        str(patient["_id"]),
        field,
        data,
    )
