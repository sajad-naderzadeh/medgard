from datetime import datetime, timezone


class SecurityMonitor:
    def record_event(
        self,
        event_type: str,
        severity: str,
        details: dict | None = None,
    ) -> dict:
        return {
            "event_type": event_type,
            "severity": severity,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc),
        }

    def suspicious_login(
        self,
        user_id: str,
        ip_address: str,
    ) -> dict:
        return self.record_event(
            event_type="suspicious_login",
            severity="high",
            details={
                "user_id": user_id,
                "ip_address": ip_address,
            },
        )
