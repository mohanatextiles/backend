"""
Products Router
===============
API endpoints for product operations
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product import ProductService
from app.services.auth import get_current_admin

router = APIRouter(prefix="/api/products", tags=["Products"])


# ============== PUBLIC ENDPOINTS ==============

@router.get("", response_model=List[ProductResponse])
async def get_products(
    category: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get enabled products (public)"""
    if category:
        products = await ProductService.get_products_by_category(db, category)
    else:
        products = await ProductService.get_enabled_products(db)
    
    return [ProductResponse(**p.to_dict()) for p in products]


@router.get("/stats")
async def get_product_stats(db: AsyncSession = Depends(get_db)):
    """Get product statistics for dashboard"""
    return await ProductService.get_product_stats(db)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    """Get single product by ID"""
    product = await ProductService.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product.to_dict())


# ============== ADMIN ENDPOINTS ==============

@router.get("/admin/all", response_model=List[ProductResponse])
async def get_all_products(
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Get all products including disabled (admin only)"""
    products = await ProductService.get_all_products(db)
    return [ProductResponse(**p.to_dict()) for p in products]


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    image_data: str = "",
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Create a new product (admin only)"""
    new_product = await ProductService.create_product(db, product, image_data)
    return ProductResponse(**new_product.to_dict())


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update a product (admin only)"""
    updated = await ProductService.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**updated.to_dict())


@router.patch("/{product_id}/toggle-enabled")
async def toggle_product_enabled(
    product_id: str,
    enabled: bool,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Toggle product enabled status (admin only)"""
    success = await ProductService.toggle_enabled(db, product_id, enabled)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True}


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Delete a product (admin only)"""
    success = await ProductService.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True}
