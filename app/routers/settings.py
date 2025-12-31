"""
Settings Router
===============
API endpoints for site settings
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.settings import SettingsUpdate, SettingsResponse
from app.services.settings import SettingsService
from app.services.auth import get_current_admin

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("", response_model=SettingsResponse)
async def get_settings(db: AsyncSession = Depends(get_db)):
    """Get site settings (public)"""
    settings = await SettingsService.get_settings(db)
    return SettingsResponse(**settings.to_dict())


@router.put("", response_model=SettingsResponse)
async def update_settings(
    data: SettingsUpdate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_admin)
):
    """Update site settings (admin only)"""
    settings = await SettingsService.update_settings(db, data)
    return SettingsResponse(**settings.to_dict())
