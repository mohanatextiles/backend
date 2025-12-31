"""
Admin Model
===========
Database model for admin users
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100), default="")
    is_admin = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "displayName": self.display_name,
            "isAdmin": self.is_admin,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
