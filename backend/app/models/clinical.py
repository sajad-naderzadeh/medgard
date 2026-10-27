from datetime import datetime, timezone
from bson import ObjectId


def base_record() -> dict:
    return {
        "_id": ObjectId(),
        "created_at": datetime.now(timezone.utc),
    }


class VitalSignModel:
    @staticmethod
    def create(data: dict) -> dict:
        return {
            **base_record(),
            **data,
        }


class LabResultModel:
    @staticmethod
    def create(data: dict) -> dict:
        return {
            **base_record(),
            **data,
        }


class ClinicalObservationModel:
    @staticmethod
    def create(data: dict) -> dict:
        return {
            **base_record(),
            **data,
        }


class PrescriptionModel:
    @staticmethod
    def create(data: dict) -> dict:
        return {
            **base_record(),
            **data,
        }
