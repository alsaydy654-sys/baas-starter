# Architecture — F0 Foundation

## Selected stack
FastAPI serves a small Python API. SQLAlchemy 2.x with `asyncpg` provides the PostgreSQL connection layer. React provides the dashboard shell. Docker Compose runs PostgreSQL 16, the API, and the frontend independently. This stack is open-source, self-hostable, and does not depend on Supabase.

## Runtime flow
`React dashboard → FastAPI /api/health (or /health directly) → SQLAlchemy async engine → PostgreSQL SELECT 1`.

The backend validates `DATABASE_URL`, `APP_ENV`, `API_PORT`, and `FRONTEND_URL` during import. Each request receives or preserves `X-Request-ID`; responses include baseline security headers. Database status is reported without exposing connection details.

## Containers and configuration
`infrastructure/docker-compose.yml` defines a PostgreSQL health check, a backend that waits for it, and a frontend. Secrets are supplied through environment variables; `.env.example` documents local names only. No database schema or migrations are created in F0 because no product data model exists yet.

## Extension points
The settings module, async engine, health service, and directory separation are intentionally small seams for future phases. Authentication, tenancy, authorization/RLS, storage, realtime, functions, billing, and external services are explicitly not present.