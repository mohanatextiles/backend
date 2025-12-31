"""
Database Configuration
======================
SQLAlchemy async setup for Neon PostgreSQL
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Base class for models (must be defined before imports)
Base = declarative_base()

# Create async engine with PostgreSQL optimized settings
engine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    # Import models to register them with Base
    from app.models import Admin, Category, Product, SiteSettings
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"✅ Created tables: {', '.join(Base.metadata.tables.keys())}")
