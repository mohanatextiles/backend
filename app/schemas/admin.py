"""
Admin Schemas
=============
Pydantic models for admin authentication
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AdminCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    display_name: Optional[str] = ""


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AdminResponse(BaseModel):
    id: str
    email: str
    displayName: str
    isAdmin: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AdminResponse
