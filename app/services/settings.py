"""
Settings Service
================
Business logic for site settings
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.settings import SiteSettings
from app.schemas.settings import SettingsUpdate


class SettingsService:
    """Settings service for site configuration"""
    
    @staticmethod
    async def get_settings(db: AsyncSession) -> SiteSettings:
        """Get site settings, creating default if not exists"""
        result = await db.execute(select(SiteSettings).where(SiteSettings.id == 1))
        settings = result.scalar_one_or_none()
        
        if not settings:
            # Create default settings
            settings = SiteSettings(
                id=1,
                homepage_enabled=True,
                products_page_enabled=True,
                site_name="Mohona Textiles",
                site_description="Premium quality clothing for men and women",
                drive_folder_id="1ms1u6tuw22Bsl1SsGpR1zXtkR_zsgddx",
            )
            db.add(settings)
            await db.commit()
            await db.refresh(settings)
        
        return settings
    
    @staticmethod
    async def update_settings(db: AsyncSession, data: SettingsUpdate) -> SiteSettings:
        """Update site settings"""
        settings = await SettingsService.get_settings(db)
        
        update_data = data.model_dump(exclude_unset=True)
        
        # Map camelCase to snake_case
        field_mapping = {
            "homepageEnabled": "homepage_enabled",
            "productsPageEnabled": "products_page_enabled",
            "siteName": "site_name",
            "siteDescription": "site_description",
            "driveFolderId": "drive_folder_id",
        }
        
        for camel_key, snake_key in field_mapping.items():
            if camel_key in update_data:
                setattr(settings, snake_key, update_data[camel_key])
        
        await db.commit()
        await db.refresh(settings)
        return settings
