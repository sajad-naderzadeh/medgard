import re


class PIIProtector:
    EMAIL_PATTERN = re.compile(
        r"([A-Za-z0-9._%+-]+)@"
        r"([A-Za-z0-9.-]+\.[A-Za-z]{2,})"
    )

    PHONE_PATTERN = re.compile(
        r"\b\d{7,15}\b"
    )

    def mask(self, text: str) -> str:
        text = self.EMAIL_PATTERN.sub(
            r"***@\2",
            text,
        )

        text = self.PHONE_PATTERN.sub(
            "***",
            text,
        )

        return text

    def redact_dict(
        self,
        data: dict,
        sensitive_fields: set[str],
    ) -> dict:
        result = data.copy()

        for field in sensitive_fields:
            if field in result:
                result[field] = "[REDACTED]"

        return result
