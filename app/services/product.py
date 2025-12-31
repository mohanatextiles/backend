"""
Product Service
===============
Business logic for product operations
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import func

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Product service for CRUD operations"""
    
    @staticmethod
    def calculate_final_price(price: float, discount: float) -> float:
        """Calculate final price after discount"""
        if discount > 0:
            return price - (price * discount / 100)
        return price
    
    @staticmethod
    async def get_enabled_products(db: AsyncSession) -> List[Product]:
        """Get all enabled products for customer view"""
        result = await db.execute(
            select(Product)
            .where(Product.enabled == True)
            .order_by(Product.created_at.desc())
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_products_by_category(db: AsyncSession, category: str) -> List[Product]:
        """Get enabled products by category"""
        result = await db.execute(
            select(Product)
            .where(Product.enabled == True, Product.category == category)
            .order_by(Product.created_at.desc())
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_product_by_id(db: AsyncSession, product_id: str) -> Optional[Product]:
        """Get single product by ID"""
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_products(db: AsyncSession) -> List[Product]:
        """Get all products for admin view"""
        result = await db.execute(
            select(Product).order_by(Product.created_at.desc())
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def create_product(
        db: AsyncSession, 
        data: ProductCreate, 
        image_data: str
    ) -> Product:
        """Create a new product"""
        final_price = ProductService.calculate_final_price(data.price, data.discount)
        
        # Convert colors to dict format
        colors_data = [{"name": c.name, "hex": c.hex} for c in data.colors]
        
        product = Product(
            name=data.name,
            category=data.category,
            price=data.price,
            discount=data.discount,
            final_price=final_price,
            description=data.description,
            image_data=image_data,
            enabled=data.enabled,
            sizes=data.sizes,
            colors=colors_data,
        )
        
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    
    @staticmethod
    async def update_product(
        db: AsyncSession,
        product_id: str,
        data: ProductUpdate
    ) -> Optional[Product]:
        """Update an existing product"""
        product = await ProductService.get_product_by_id(db, product_id)
        if not product:
            return None
        
        # Update fields that are provided
        update_data = data.model_dump(exclude_unset=True)
        
        # Handle colors conversion if provided
        if "colors" in update_data and update_data["colors"]:
            update_data["colors"] = [{"name": c["name"], "hex": c["hex"]} for c in update_data["colors"]]
        
        # Recalculate final price if price or discount changed
        price = update_data.get("price", product.price)
        discount = update_data.get("discount", product.discount)
        update_data["final_price"] = ProductService.calculate_final_price(price, discount)
        
        for key, value in update_data.items():
            setattr(product, key, value)
        
        await db.commit()
        await db.refresh(product)
        return product
    
    @staticmethod
    async def toggle_enabled(db: AsyncSession, product_id: str, enabled: bool) -> bool:
        """Toggle product enabled status"""
        result = await db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(enabled=enabled, updated_at=func.now())
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def delete_product(db: AsyncSession, product_id: str) -> bool:
        """Delete a product"""
        result = await db.execute(
            delete(Product).where(Product.id == product_id)
        )
        await db.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def get_product_stats(db: AsyncSession) -> dict:
        """Get product statistics for dashboard"""
        total = await db.execute(select(func.count(Product.id)))
        enabled = await db.execute(select(func.count(Product.id)).where(Product.enabled == True))
        
        categories_result = await db.execute(
            select(Product.category).distinct()
        )
        categories = [c[0] for c in categories_result.fetchall()]
        
        return {
            "totalProducts": total.scalar() or 0,
            "enabledProducts": enabled.scalar() or 0,
            "categories": categories,
        }
