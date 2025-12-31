"""
Categories Router
=================
API endpoints for category operations
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category import CategoryService
from app.services.auth import get_current_admin

router = APIRouter(prefix="/api/categories", tags=["Categories"])


# ============== PUBLIC ENDPOINTS ==============

@router.get("", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all enabled categories (public)"""
    categories = await CategoryService.get_enabled_categories(db)
    return [CategoryResponse(**c.to_dict()) for c in categories]


# ============== ADMIN ENDPOINTS ==============

@router.get("/admin/all", response_model=List[CategoryResponse])
async def get_all_categories(
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all categories including disabled (admin only)"""
    categories = await CategoryService.get_all_categories(db)
    return [CategoryResponse(**c.to_dict()) for c in categories]


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Create a new category (admin only)"""
    # Check if slug already exists
    existing = await CategoryService.get_category_by_slug(db, category.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this slug already exists"
        )
    
    new_category = await CategoryService.create_category(
        db, category.name, category.slug, category.description or ""
    )
    return CategoryResponse(**new_category.to_dict())


@router.delete("/{category_id}")
async def delete_category(
    category_id: str,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Delete a category (admin only)"""
    success = await CategoryService.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True}


@router.post("/seed")
async def seed_categories(
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Seed default categories (admin only)"""
    categories = await CategoryService.seed_default_categories(db)
    return [CategoryResponse(**c.to_dict()) for c in categories]
