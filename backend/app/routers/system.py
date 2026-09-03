from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["System"])

@router.get("/system/status")
async def system_status(db: AsyncSession = Depends(get_db)):
    db_version = "unknown"
    try:
        res = await db.execute(text("SHOW server_version;"))
        db_version = res.scalar() or "unknown"
    except Exception as e:
        db_version = f"Error: {str(e)}"
        
    return {
        "platform": settings.PROJECT_NAME,
        "phase": "F0 - Foundation Only",
        "environment": settings.ENVIRONMENT,
        "database_version": db_version,
        "features_enabled": [
            "postgresql_connection_pool",
            "health_check_endpoint",
            "request_correlation_id",
            "structured_logging",
            "docker_compose_stack"
        ],
        "features_out_of_scope": [
            "authentication",
            "billing",
            "storage",
            "realtime",
            "ai_features"
        ]
    }
