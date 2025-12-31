"""
Database Migration Script
=========================
Recreates tables with new schema (image_data instead of image_url)
"""

import asyncio
from app.database import engine, Base
from app.models import Product, Category, Admin, SiteSettings


async def recreate_tables():
    """Drop and recreate all tables"""
    print("🔄 Dropping existing tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✅ Tables dropped")
    
    print("🔄 Creating new tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ New tables created with updated schema")
    print("\nℹ️  Note: All existing data has been cleared.")
    print("ℹ️  You'll need to create a new admin account on first startup.")


if __name__ == "__main__":
    asyncio.run(recreate_tables())
