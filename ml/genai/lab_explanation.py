class LabExplanationService:

    def explain(self, lab: dict) -> dict:
        value = lab.get("value")
        minimum = lab.get("reference_min")
        maximum = lab.get("reference_max")

        status = "unknown"

        if (
            value is not None
            and minimum is not None
            and maximum is not None
        ):
            if value < minimum:
                status = "below_reference"
            elif value > maximum:
                status = "above_reference"
            else:
                status = "within_reference"

        return {
            "test_name": lab.get("test_name"),
            "value": value,
            "unit": lab.get("unit"),
            "reference_range": {
                "min": minimum,
                "max": maximum,
            },
            "status": status,
            "explanation": (
                "Reference-range classification only. "
                "Clinical interpretation requires "
                "appropriate medical context."
            ),
        }
