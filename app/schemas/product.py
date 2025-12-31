"""
Product Schemas
===============
Pydantic models for product API validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ColorVariantSchema(BaseModel):
    name: str
    hex: str


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    discount: float = Field(default=0, ge=0, le=100)
    description: str = ""
    enabled: bool = True
    sizes: List[str] = ["S", "M", "L", "XL"]
    colors: List[ColorVariantSchema] = [{"name": "Black", "hex": "#000000"}]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[ColorVariantSchema]] = None
    image_data: Optional[str] = None


class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    price: float
    discount: float
    finalPrice: float
    description: str
    imageData: str
    enabled: bool
    sizes: List[str]
    colors: List[dict]
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    
    class Config:
        from_attributes = True
