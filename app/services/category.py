"""
Category Service
================
Business logic for category operations
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.category import Category
from app.schemas.category import CategoryCreate


class CategoryService:
    """Category service for CRUD operations"""
    
    @staticmethod
    async def get_enabled_categories(db: AsyncSession) -> List[Category]:
        """Get all enabled categories for customer view"""
        result = await db.execute(
            select(Category)
            .where(Category.enabled == True)
            .order_by(Category.name)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_all_categories(db: AsyncSession) -> List[Category]:
        """Get all categories for admin view"""
        result = await db.execute(
            select(Category).order_by(Category.created_at.desc())
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_category_by_id(db: AsyncSession, category_id: str) -> Optional[Category]:
        """Get category by ID"""
        result = await db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_category_by_slug(db: AsyncSession, slug: str) -> Optional[Category]:
        """Get category by slug"""
        result = await db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_category(
        db: AsyncSession,
        name: str,
        slug: str,
        description: str = ""
    ) -> Category:
        """Create a new category"""
        category = Category(
            name=name,
            slug=slug,
            description=description,
            enabled=True,
        )
        
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category
    
    @staticmethod
    async def delete_category(db: AsyncSession, category_id: str) -> bool:
        """Delete a category"""
        result = await db.execute(
            delete(Category).where(Category.id == category_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def seed_default_categories(db: AsyncSession) -> List[Category]:
        """Seed default categories if none exist"""
        existing = await CategoryService.get_all_categories(db)
        if existing:
            return existing
        
        default_categories = [
            {"name": "Men's", "slug": "mens", "description": "Clothing for men"},
            {"name": "Women's", "slug": "womens", "description": "Clothing for women"},
            {"name": "Accessories", "slug": "accessories", "description": "Fashion accessories"},
            {"name": "Kids", "slug": "kids", "description": "Clothing for children"},
        ]
        
        categories = []
        for cat in default_categories:
            category = await CategoryService.create_category(
                db, cat["name"], cat["slug"], cat["description"]
            )
            categories.append(category)
        
        return categories
