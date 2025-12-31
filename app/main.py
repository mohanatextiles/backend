"""
FastAPI Application
===================
Mohana Textiles E-commerce Backend
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database import init_db
from app.routers import (
    auth_router,
    products_router,
    categories_router,
    settings_router,
)
from app.routers.ai_products import router as ai_products_router
from app.routers.images import router as images_router


# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_production else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown"""
    logger.info("Starting Mohana Textiles API")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized successfully")
    logger.info("Server ready")
    
    yield
    
    logger.info("Server shutdown complete")


# Create app
app = FastAPI(
    title="Mohana Textiles API",
    description="E-commerce backend for Mohana Textiles",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - Configure based on environment
if settings.is_production:
    # Production: Strict CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
else:
    # Development: Relaxed CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routes
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(settings_router)
app.include_router(ai_products_router)
app.include_router(images_router)


@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "message": "Mohana Textiles API"}


@app.get("/api/health")
async def health():
    """API health check"""
    return {"status": "ok"}
