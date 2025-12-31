"""
Authentication Router
=====================
Simple token-based admin authentication
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.admin import AdminLogin, AdminResponse, Token
from app.services.auth import AuthService, get_current_admin
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


@router.post("/login", response_model=Token)
async def login(credentials: AdminLogin, db: AsyncSession = Depends(get_db)):
    """Admin login - returns token"""
    admin = await AuthService.authenticate_admin(db, credentials.email, credentials.password)
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Generate simple token
    token = AuthService.create_session(admin.id, admin.email)
    
    return Token(
        access_token=token,
        token_type="bearer",
        user=AdminResponse(
            id=admin.id,
            email=admin.email,
            displayName=admin.display_name or "",
            isAdmin=admin.is_admin,
        ),
    )


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout - invalidate token"""
    if credentials:
        AuthService.invalidate_token(credentials.credentials)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=AdminResponse)
async def get_me(
    session: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get current admin info"""
    admin = await AuthService.get_admin_by_id(db, session["admin_id"])
    
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
        )
    
    return AdminResponse(
        id=admin.id,
        email=admin.email,
        displayName=admin.display_name or "",
        isAdmin=admin.is_admin,
    )


@router.get("/config")
async def get_config():
    """Get public config (Drive folder URL)"""
    return {
        "driveFolderUrl": settings.google_drive_folder_url
    }
