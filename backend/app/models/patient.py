from datetime import datetime, timezone
from bson import ObjectId


class PatientModel:
    collection = "patients"

    @staticmethod
    def create_document(
        user_id: str,
        date_of_birth: str | None = None,
        gender: str | None = None,
        blood_type: str | None = None,
    ) -> dict:
        now = datetime.now(timezone.utc)

        return {
            "_id": ObjectId(),
            "user_id": ObjectId(user_id),
            "date_of_birth": date_of_birth,
            "gender": gender,
            "blood_type": blood_type,
            "medical_history": [],
            "family_history": [],
            "allergies": [],
            "chronic_conditions": [],
            "diagnoses": [],
            "medications": [],
            "vital_signs": [],
            "lab_results": [],
            "clinical_notes": [],
            "medical_events": [],
            "created_at": now,
            "updated_at": now,
        }
