from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    Usa pydantic-settings para carregar variáveis de ambiente (suporte a .env automático).
    """
    DB_URL: str = Field(
        default="postgresql+asyncpg://workout:workout@localhost:5432/workout",
        description="URL de conexão com o banco PostgreSQL (async)"
    )
    DB_ECHO: bool = Field(default=False, description="Habilita logs SQL detalhados")

    class Config:
        env_file = ".env"  # Carrega automaticamente de .env se existir


settings = Settings()