from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from settings import settings
from sqlalchemy.pool import NullPool

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    poolclass=NullPool
)

SessionLocal = async_sessionmaker(autocommit=False,
                                  autoflush=False,
                                  expire_on_commit=False,
                                  bind=engine)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
