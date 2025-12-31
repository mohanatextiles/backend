# API Routers
from app.routers.auth import router as auth_router
from app.routers.products import router as products_router
from app.routers.categories import router as categories_router
from app.routers.settings import router as settings_router

__all__ = [
    "auth_router",
    "products_router",
    "categories_router",
    "settings_router",
]
