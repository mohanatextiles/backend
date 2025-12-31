"""
Settings Schemas
================
Pydantic models for site settings
"""

from pydantic import BaseModel
from typing import Optional


class SettingsUpdate(BaseModel):
    homepageEnabled: Optional[bool] = None
    productsPageEnabled: Optional[bool] = None
    siteName: Optional[str] = None
    siteDescription: Optional[str] = None
    driveFolderId: Optional[str] = None


class SettingsResponse(BaseModel):
    homepageEnabled: bool
    productsPageEnabled: bool
    siteName: str
    siteDescription: str
    driveFolderId: str
    
    class Config:
        from_attributes = True
