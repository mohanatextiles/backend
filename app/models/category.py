"""
Category Model
==============
Database model for product categories
"""

from sqlalchemy import Column, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, default="")
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "enabled": self.enabled,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
