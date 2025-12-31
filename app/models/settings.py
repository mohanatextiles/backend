"""
Site Settings Model
===================
Database model for site-wide settings
"""

from sqlalchemy import Column, String, Boolean, Text, Integer
from app.database import Base


class SiteSettings(Base):
    __tablename__ = "site_settings"
    
    id = Column(Integer, primary_key=True, default=1)  # Single row for settings
    homepage_enabled = Column(Boolean, default=True)
    products_page_enabled = Column(Boolean, default=True)
    site_name = Column(String(255), default="Mohona Textiles")
    site_description = Column(Text, default="Premium quality clothing for men and women")
    
    # Google Drive folder for product images
    drive_folder_id = Column(String(255), default="1ms1u6tuw22Bsl1SsGpR1zXtkR_zsgddx")
    
    def to_dict(self):
        return {
            "homepageEnabled": self.homepage_enabled,
            "productsPageEnabled": self.products_page_enabled,
            "siteName": self.site_name,
            "siteDescription": self.site_description,
            "driveFolderId": self.drive_folder_id,
        }
