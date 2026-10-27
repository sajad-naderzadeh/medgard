from pydantic import BaseModel, Field


class VitalSignsCreate(BaseModel):
    blood_pressure_systolic: float | None = Field(default=None, ge=40, le=300)
    blood_pressure_diastolic: float | None = Field(default=None, ge=20, le=200)
    heart_rate: float | None = Field(default=None, ge=20, le=250)
    temperature: float | None = Field(default=None, ge=25, le=45)
    oxygen_saturation: float | None = Field(default=None, ge=50, le=100)
    respiratory_rate: float | None = Field(default=None, ge=5, le=80)
    weight_kg: float | None = Field(default=None, ge=1, le=500)
    height_cm: float | None = Field(default=None, ge=30, le=250)


class LabResultCreate(BaseModel):
    test_name: str = Field(min_length=1, max_length=200)
    value: float
    unit: str = Field(min_length=1, max_length=50)
    reference_min: float | None = None
    reference_max: float | None = None
    status: str = Field(default="normal", max_length=50)
    tested_at: str | None = None


class ClinicalObservationCreate(BaseModel):
    observation_type: str = Field(min_length=1, max_length=100)
    value: str = Field(min_length=1, max_length=500)
    notes: str | None = Field(default=None, max_length=2000)


class PrescriptionCreate(BaseModel):
    medication_name: str = Field(min_length=1, max_length=200)
    dosage: str = Field(min_length=1, max_length=100)
    frequency: str = Field(min_length=1, max_length=100)
    duration: str | None = Field(default=None, max_length=100)
    instructions: str | None = Field(default=None, max_length=2000)


class MedicalDocumentCreate(BaseModel):
    document_type: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=300)
    document_url: str | None = None


class DiagnosisUpdate(BaseModel):
    diagnosis: str = Field(min_length=1, max_length=200)
    status: str = Field(default="active", max_length=50)
    notes: str | None = Field(default=None, max_length=2000)
