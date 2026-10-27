from datetime import datetime

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    date_of_birth: str | None = None
    gender: str | None = Field(default=None, max_length=50)
    blood_type: str | None = Field(default=None, max_length=10)


class PatientResponse(BaseModel):
    id: str
    user_id: str
    date_of_birth: str | None
    gender: str | None
    blood_type: str | None
    created_at: datetime
    updated_at: datetime


class MedicalHistoryCreate(BaseModel):
    condition: str = Field(min_length=1, max_length=200)
    diagnosed_at: str | None = None
    notes: str | None = Field(default=None, max_length=2000)


class AllergyCreate(BaseModel):
    allergen: str = Field(min_length=1, max_length=200)
    reaction: str | None = Field(default=None, max_length=500)
    severity: str | None = Field(default=None, max_length=50)


class ChronicConditionCreate(BaseModel):
    condition: str = Field(min_length=1, max_length=200)
    diagnosed_at: str | None = None
    status: str = Field(default="active", max_length=50)


class DiagnosisCreate(BaseModel):
    diagnosis: str = Field(min_length=1, max_length=200)
    diagnosed_at: str | None = None
    notes: str | None = Field(default=None, max_length=2000)


class MedicationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    dosage: str | None = None
    frequency: str | None = None
    started_at: str | None = None


class ClinicalNoteCreate(BaseModel):
    note: str = Field(min_length=1, max_length=10000)
    author: str | None = None


class MedicalEventCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=2000)
    event_date: str | None = None
