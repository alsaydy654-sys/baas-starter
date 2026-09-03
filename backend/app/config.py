import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Emergent BaaS Platform (F0)"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/emergent_f0"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
