from fastapi import HTTPException, status

from app.models.clinical import (
    ClinicalObservationModel,
    LabResultModel,
    PrescriptionModel,
    VitalSignModel,
)
from app.repositories.clinical import ClinicalRepository
from app.repositories.patient import PatientRepository


async def get_patient_id(user_id: str) -> str:
    patient = await PatientRepository.find_by_user_id(user_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found",
        )

    return str(patient["_id"])


async def add_vital_signs(user_id: str, data):
    patient_id = await get_patient_id(user_id)

    document = VitalSignModel.create(
        data.model_dump()
    )

    return await ClinicalRepository.push(
        patient_id,
        "vital_signs",
        document,
    )


async def add_lab_result(user_id: str, data):
    patient_id = await get_patient_id(user_id)

    document = LabResultModel.create(
        data.model_dump()
    )

    return await ClinicalRepository.push(
        patient_id,
        "lab_results",
        document,
    )


async def add_observation(user_id: str, data):
    patient_id = await get_patient_id(user_id)

    document = ClinicalObservationModel.create(
        data.model_dump()
    )

    return await ClinicalRepository.push(
        patient_id,
        "clinical_observations",
        document,
    )


async def add_prescription(user_id: str, data):
    patient_id = await get_patient_id(user_id)

    document = PrescriptionModel.create(
        data.model_dump()
    )

    return await ClinicalRepository.push(
        patient_id,
        "prescriptions",
        document,
    )


async def get_clinical_records(
    user_id: str,
    field: str,
):
    patient_id = await get_patient_id(user_id)

    return await ClinicalRepository.get_records(
        patient_id,
        field,
    )
