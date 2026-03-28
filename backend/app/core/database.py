from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# The engine is the connection pool — create once, reuse forever
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,        # set True to log SQL queries (great for debugging)
    pool_size=10,
    max_overflow=20,
)

# Factory that creates database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # objects stay usable after commit
)

# Base class all models inherit from
class Base(DeclarativeBase):
    pass