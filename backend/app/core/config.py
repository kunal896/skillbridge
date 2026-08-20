from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SkillBridge API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://skillbridge:skillbridge@localhost:5432/skillbridge"
    frontend_url: str = "http://localhost:3000"
    jwt_secret_key: str = "CHANGE_ME_IN_ENV"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    anthropic_api_key: str | None = None
    adzuna_app_id: str | None = None
    adzuna_app_key: str | None = None
    judge0_api_url: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
