from datetime import datetime, timezone
from app.core.database import get_database


class AuditLogService:
    async def log(
        self,
        action: str,
        user_id: str | None = None,
        resource: str | None = None,
        resource_id: str | None = None,
        metadata: dict | None = None,
    ):
        db = get_database()

        document = {
            "action": action,
            "user_id": user_id,
            "resource": resource,
            "resource_id": resource_id,
            "metadata": metadata or {},
            "created_at": datetime.now(timezone.utc),
        }

        await db.audit_logs.insert_one(document)

        return document
