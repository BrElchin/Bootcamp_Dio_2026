from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    database_url: str
    environment: str = "development"

    # JWT settings
    jwt_secret: str = "my-super-secret-key-change-in-production"  # Mude para algo forte!
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30  # Tempo de vida do token

settings = Settings()
