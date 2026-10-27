from bson import ObjectId

from app.core.database import get_database


class PatientRepository:

    @staticmethod
    async def find_by_user_id(user_id: str):
        db = get_database()

        return await db.patients.find_one(
            {"user_id": ObjectId(user_id)}
        )

    @staticmethod
    async def find_by_id(patient_id: str):
        db = get_database()

        return await db.patients.find_one(
            {"_id": ObjectId(patient_id)}
        )

    @staticmethod
    async def create(document: dict):
        db = get_database()

        result = await db.patients.insert_one(document)

        return await db.patients.find_one(
            {"_id": result.inserted_id}
        )

    @staticmethod
    async def update(patient_id: str, data: dict):
        db = get_database()

        await db.patients.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": data},
        )

        return await PatientRepository.find_by_id(patient_id)

    @staticmethod
    async def push(
        patient_id: str,
        field: str,
        data: dict,
    ):
        db = get_database()

        await db.patients.update_one(
            {"_id": ObjectId(patient_id)},
            {"$push": {field: data}},
        )

        return await PatientRepository.find_by_id(patient_id)
