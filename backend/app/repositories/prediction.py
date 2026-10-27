from typing import Any

from app.core.database import get_database


class PredictionRepository:

    async def create(self, prediction: dict[str, Any]) -> dict[str, Any]:
        db = get_database()

        result = await db.predictions.insert_one(prediction)
        prediction["_id"] = str(result.inserted_id)

        return prediction

    async def get_by_patient(
        self,
        patient_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        db = get_database()

        cursor = (
            db.predictions
            .find({"patient_id": patient_id})
            .sort("created_at", -1)
            .limit(limit)
        )

        records = await cursor.to_list(length=limit)

        for record in records:
            record["_id"] = str(record["_id"])

        return records
