"""
Product Model
=============
Database model for products
"""

from sqlalchemy import Column, String, Float, Boolean, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    final_price = Column(Float, nullable=False)
    description = Column(Text, default="")
    image_data = Column(Text, default="")  # Store base64 encoded image
    enabled = Column(Boolean, default=True, index=True)
    sizes = Column(JSON, default=list)  # Store as JSON array
    colors = Column(JSON, default=list)  # Store as JSON array of {name, hex}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "discount": self.discount,
            "finalPrice": self.final_price,
            "description": self.description,
            "imageData": self.image_data,
            "enabled": self.enabled,
            "sizes": self.sizes or [],
            "colors": self.colors or [],
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }


class ColorVariant(Base):
    """Separate table for color variants if needed"""
    __tablename__ = "color_variants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    hex = Column(String(7), nullable=False)
