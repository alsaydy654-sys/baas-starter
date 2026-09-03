import os
import pytest
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/emergent_f0")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("API_PORT", "8001")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")

from backend.server import app


@pytest.mark.asyncio
async def test_health_contract():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert {"status", "environment", "timestamp", "database", "request_id"} <= response.json().keys()


@pytest.mark.asyncio
async def test_ingress_health_alias():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/health")
    assert response.status_code == 200


def test_no_supabase_dependency_in_backend():
    requirements = open("backend/requirements.txt").read().lower()
    assert "supabase" not in requirements