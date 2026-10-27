from datetime import datetime, timezone
from enum import Enum

from bson import ObjectId


class UserRole(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    PATIENT = "patient"


class UserModel:
    collection = "users"

    @staticmethod
    def create_document(
        email: str,
        hashed_password: str,
        role: UserRole = UserRole.PATIENT,
        first_name: str = "",
        last_name: str = "",
    ) -> dict:
        now = datetime.now(timezone.utc)

        return {
            "_id": ObjectId(),
            "email": email.lower().strip(),
            "hashed_password": hashed_password,
            "role": role.value,
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
