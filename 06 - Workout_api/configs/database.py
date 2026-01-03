from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings


# Cria o engine assíncrono com echo controlado pela settings
engine = create_async_engine(settings.DB_URL, echo=settings.DB_ECHO)

# Session factory assíncrona
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency que fornece uma sessão assíncrona com o banco de dados.
    Uso em FastAPI: Depends(get_session)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()