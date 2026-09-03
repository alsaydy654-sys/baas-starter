# Security Baseline — F0

- No authentication, authorization, tenants, RLS, users, or secrets are implemented.
- Required runtime configuration fails fast when missing.
- `.gitignore` excludes `.env`, logs, build output, caches, and local database volumes; `.env.example` contains no secret.
- CORS is restricted to `FRONTEND_URL`.
- Responses add `X-Content-Type-Options`, `X-Frame-Options`, and `Referrer-Policy`.
- Request IDs and structured request events support basic tracing.

This is a development foundation and **not production secure**. TLS, secret management, authentication, authorization, rate limiting, and full observability belong to later work.