from bson import ObjectId

from app.core.database import get_database


class ClinicalRepository:

    @staticmethod
    async def get_patient(patient_id: str):
        db = get_database()

        return await db.patients.find_one(
            {"_id": ObjectId(patient_id)}
        )

    @staticmethod
    async def push(
        patient_id: str,
        field: str,
        document: dict,
    ):
        db = get_database()

        await db.patients.update_one(
            {"_id": ObjectId(patient_id)},
            {
                "$push": {
                    field: document
                }
            },
        )

        return await ClinicalRepository.get_patient(patient_id)

    @staticmethod
    async def get_records(
        patient_id: str,
        field: str,
    ):
        patient = await ClinicalRepository.get_patient(patient_id)

        if not patient:
            return []

        return patient.get(field, [])
