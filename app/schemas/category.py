"""
Category Schemas
================
Pydantic models for category API validation
"""

from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = ""


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    enabled: bool
    createdAt: Optional[str] = None
    
    class Config:
        from_attributes = True
