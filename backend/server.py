"""F0 backend: a small, independently deployable PostgreSQL health service."""
from datetime import datetime, timezone
import logging
import os
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class Settings(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    app_env: str = Field(validation_alias="APP_ENV")
    api_port: int = Field(validation_alias="API_PORT")
    frontend_url: str = Field(validation_alias="FRONTEND_URL")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
engine: AsyncEngine = create_async_engine(settings.database_url, pool_pre_ping=True)
logger = logging.getLogger("f0.backend")
logging.basicConfig(level=logging.INFO, format="%(message)s")


class HealthResponse(BaseModel):
    status: str
    environment: str
    timestamp: datetime
    database: str
    request_id: str


app = FastAPI(title="Emergent BaaS F0 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    try:
        response = await call_next(request)
    except Exception:
        logger.exception('{"event":"request.error","request_id":"%s"}', request_id)
        return JSONResponse(status_code=500, content={"detail": "Internal server error", "request_id": request_id})
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    logger.info('{"event":"request.completed","request_id":"%s","method":"%s","path":"%s","status":%s}', request_id, request.method, request.url.path, response.status_code)
    return response


async def check_database() -> str:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return "connected"
    except (SQLAlchemyError, OSError):
        return "unavailable"


@app.get("/health", response_model=HealthResponse)
@app.get("/api/health", response_model=HealthResponse, include_in_schema=False)
async def health(request: Request):
    request_id = request.headers.get("X-Request-ID", "") or str(uuid.uuid4())
    database = await check_database()
    return HealthResponse(
        status="ok" if database == "connected" else "degraded",
        environment=settings.app_env,
        timestamp=datetime.now(timezone.utc),
        database=database,
        request_id=request_id,
    )


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()