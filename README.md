# Emergent BaaS Alternative — F0 Foundation

An independently deployable backend foundation centered on PostgreSQL. This is **not a Supabase clone** and does not depend on Supabase.

## Run locally with Docker

```bash
cp .env.example .env
docker compose -f infrastructure/docker-compose.yml up --build
```

- Dashboard: http://localhost:3000
- Backend health: http://localhost:8001/health (or `/api/health` through the hosted ingress)
- PostgreSQL: localhost:5432

## Run backend tests

```bash
pip install -r backend/requirements.txt
pytest tests -q
```

## Required configuration

`DATABASE_URL`, `APP_ENV`, `API_PORT`, and `FRONTEND_URL` are required by the backend. PostgreSQL container variables are documented in `.env.example`. Never commit a real `.env`.

## Scope

F0 includes only runtime architecture, a PostgreSQL connection probe, `/health`, structured request IDs, a minimal status dashboard, Docker Compose, tests, and documentation. Authentication, billing, storage, realtime, AI, external integrations, tenants, RLS, users, and product schemas are **NOT IMPLEMENTED — F0**.