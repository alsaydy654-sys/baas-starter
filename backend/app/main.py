from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.logging import setup_logging, RequestLoggingMiddleware
from app.routers import health, system

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0-F0",
    description="Emergent BaaS Platform - Phase F0 Foundation",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(system.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Emergent BaaS Platform (F0 Foundation)",
        "docs": "/docs",
        "health": "/health",
        "system_status": "/api/v1/system/status"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
