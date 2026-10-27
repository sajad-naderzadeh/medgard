class PatientSummarizer:
    def summarize(self, patient: dict) -> dict:
        summary = {
            "demographics": {
                "age": patient.get("age"),
                "gender": patient.get("gender"),
            },
            "conditions": patient.get(
                "chronic_conditions",
                [],
            ),
            "medications": patient.get(
                "medications",
                [],
            ),
            "allergies": patient.get(
                "allergies",
                [],
            ),
            "recent_vitals": patient.get(
                "vital_signs",
                [],
            ),
            "recent_labs": patient.get(
                "lab_results",
                [],
            ),
        }

        return {
            "summary": summary,
            "disclaimer": (
                "This summary is generated from "
                "provided clinical data and is not "
                "a medical diagnosis."
            ),
        }
