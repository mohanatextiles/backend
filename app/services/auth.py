"""
Authentication Service
======================
Simple token-based authentication (no JWT complexity)
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.models.admin import Admin


security = HTTPBearer()

# In-memory token store - simple approach
# Tokens persist until server restart or manual logout
active_tokens: Dict[str, dict] = {}


class AuthService:
    """Simple token-based authentication"""
    
    TOKEN_EXPIRY_HOURS = 24
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password with SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return AuthService.hash_password(plain_password) == hashed_password
    
    @staticmethod
    def generate_token() -> str:
        """Generate random secure token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_session(admin_id: str, email: str) -> str:
        """Create session and return token"""
        token = AuthService.generate_token()
        active_tokens[token] = {
            "admin_id": admin_id,
            "email": email,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=AuthService.TOKEN_EXPIRY_HOURS)
        }
        return token
    
    @staticmethod
    def validate_token(token: str) -> Optional[dict]:
        """Validate token and return session"""
        session = active_tokens.get(token)
        if not session:
            return None
        
        if datetime.utcnow() > session["expires_at"]:
            del active_tokens[token]
            return None
        
        return session
    
    @staticmethod
    def invalidate_token(token: str) -> bool:
        """Logout - invalidate token"""
        if token in active_tokens:
            del active_tokens[token]
            return True
        return False
    
    @staticmethod
    async def authenticate_admin(db: AsyncSession, email: str, password: str) -> Optional[Admin]:
        """Authenticate admin with email/password"""
        result = await db.execute(select(Admin).where(Admin.email == email))
        admin = result.scalar_one_or_none()
        
        if not admin:
            return None
        if not AuthService.verify_password(password, admin.password_hash):
            return None
        if not admin.is_admin:
            return None
        
        return admin
    
    @staticmethod
    async def get_admin_by_id(db: AsyncSession, admin_id: str) -> Optional[Admin]:
        """Get admin by ID"""
        result = await db.execute(select(Admin).where(Admin.id == admin_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_admin_by_email(db: AsyncSession, email: str) -> Optional[Admin]:
        """Get admin by email"""
        result = await db.execute(select(Admin).where(Admin.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_admin(db: AsyncSession, email: str, password: str, display_name: str = "") -> Admin:
        """Create new admin"""
        admin = Admin(
            email=email,
            password_hash=AuthService.hash_password(password),
            display_name=display_name,
            is_admin=True,
        )
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        return admin


async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Dependency to get current admin from token"""
    token = credentials.credentials
    session = AuthService.validate_token(token)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return session
