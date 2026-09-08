# Emergent BaaS Alternative — F0 PRD

## Original problem statement

Implement the EMERGENT SUPABASE ALTERNATIVE MASTER BUILD CONTRACT V0.1, PHASE F0 — FOUNDATION ONLY. Build an independently deployable, documented, testable, containerizable, environment-driven PostgreSQL-centered foundation. Do not implement authentication, billing, storage, realtime, AI, external integrations, or any F1–F10 feature.

## Architecture decisions

- FastAPI backend with SQLAlchemy 2.x and asyncpg for PostgreSQL connectivity.
- React dashboard shell for runtime status only.
- Docker Compose for PostgreSQL 16, backend, and frontend local development.
- Pydantic Settings validates required environment variables at startup.
- `/health` is the direct backend endpoint; `/api/health` is an ingress-compatible alias.
- No product schema or migrations are created in F0.

## User personas

- Platform engineer verifying that the independent runtime starts and connects to PostgreSQL.
- Developer evaluating the repository structure, health contract, and local reproducibility.

## Core requirements (static)

- Repository separation: frontend, backend, infrastructure, docs, tests.
- PostgreSQL connection probe and safe degraded status.
- Structured request logging, correlation IDs, CORS configuration, baseline security headers.
- Developer dashboard with navigation, backend status, database status, and explicit F0 boundaries.
- Environment example, documentation, Compose configuration, automated tests, and no secrets.

## What's implemented

### 2026-09-03

- Replaced the MongoDB starter backend with FastAPI + async SQLAlchemy PostgreSQL connectivity.
- Added `/health` and `/api/health`, environment validation, correlation IDs, structured request events, and security headers.
- Built the responsive dark F0 status dashboard with unique `data-testid` values and explicit NOT IMPLEMENTED scope states.
- Added Dockerfiles, Docker Compose, `.env.example`, `.gitignore`, README, architecture/security/roadmap documentation.
- Added pytest coverage for health, ingress alias, environment validation, and no-Supabase dependency.
- Verified backend tests (4/4), frontend production build, browser dashboard flow, and static Compose configuration.
- Final F0 gate: corrected Compose frontend port mapping and POSTGRES_* interpolation; static checks, tests, scans, and browser verification passed. Docker runtime and live PostgreSQL remain NOT VERIFIED because Docker is unavailable.

## Acceptance and limitations

- Backend build: PASS
- Frontend build: PASS
- `/health` HTTP 200: PASS
- Frontend reaches backend: PASS through `/api/health`
- PostgreSQL starts/connects: NOT VERIFIED — Docker CLI is unavailable in this execution environment
- Docker Compose runtime: NOT VERIFIED — Docker CLI is unavailable
- No Supabase dependency: PASS
- No committed secrets: PASS by static configuration review
- Full automated acceptance: NOT VERIFIED until Docker is available

## Prioritized backlog

### P0 remaining

- Run the existing Compose stack in a Docker-enabled environment and verify PostgreSQL connection reports `connected`.

### P1 remaining

- None within F0. Any new capability requires a new explicit build contract.

### P2 remaining

- None within F0. Do not begin F1 without a new contract.

## Next tasks

1. Execute `docker compose -f infrastructure/docker-compose.yml up --build` in a Docker-enabled environment.
2. Confirm `http://localhost:8001/health` reports PostgreSQL `connected`.
3. Confirm the dashboard shows Backend API Reachable and PostgreSQL Connected.
4. Stop after F0 verification; do not start F1.