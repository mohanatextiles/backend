"""
Create Admin User Script
=========================
Interactive script to create additional admin users

Usage:
    python create_admin.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import AsyncSessionLocal, init_db
from app.services.auth import AuthService
import getpass


async def create_admin_user():
    """Interactive admin creation"""
    print("=" * 60)
    print("CREATE ADMIN USER".center(60))
    print("=" * 60)
    print()
    
    # Get admin details
    email = input("Enter admin email: ").strip()
    if not email:
        print("❌ Email is required!")
        return
    
    # Get password securely
    while True:
        password = getpass.getpass("Enter password: ").strip()
        if len(password) < 6:
            print("❌ Password must be at least 6 characters!")
            continue
        
        password_confirm = getpass.getpass("Confirm password: ").strip()
        if password != password_confirm:
            print("❌ Passwords don't match!")
            continue
        break
    
    display_name = input("Enter display name (optional): ").strip() or "Admin"
    
    print()
    print("Creating admin user...")
    
    try:
        # Initialize database
        await init_db()
        
        async with AsyncSessionLocal() as db:
            # Check if admin already exists
            existing = await AuthService.get_admin_by_email(db, email)
            if existing:
                print(f"❌ Admin with email '{email}' already exists!")
                return
            
            # Create admin
            admin = await AuthService.create_admin(db, email, password, display_name)
            
            print()
            print("✅ Admin user created successfully!")
            print()
            print("-" * 60)
            print(f"Email:        {admin.email}")
            print(f"Display Name: {admin.display_name}")
            print(f"Admin ID:     {admin.id}")
            print("-" * 60)
            print()
            print("You can now login at: http://localhost:5173/admin/login")
            
    except Exception as e:
        print(f"❌ Error creating admin: {str(e)}")
        import traceback
        traceback.print_exc()


async def list_admins():
    """List all admin users"""
    print("=" * 60)
    print("EXISTING ADMIN USERS".center(60))
    print("=" * 60)
    print()
    
    try:
        await init_db()
        
        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            from app.models.admin import Admin
            
            result = await db.execute(select(Admin))
            admins = result.scalars().all()
            
            if not admins:
                print("No admin users found.")
                return
            
            for i, admin in enumerate(admins, 1):
                print(f"{i}. {admin.email}")
                print(f"   Name: {admin.display_name}")
                print(f"   ID: {admin.id}")
                print(f"   Created: {admin.created_at}")
                print()
                
    except Exception as e:
        print(f"❌ Error listing admins: {str(e)}")


async def main():
    """Main menu"""
    while True:
        print()
        print("=" * 60)
        print("ADMIN USER MANAGEMENT".center(60))
        print("=" * 60)
        print()
        print("1. Create new admin user")
        print("2. List existing admins")
        print("3. Exit")
        print()
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == "1":
            await create_admin_user()
        elif choice == "2":
            await list_admins()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
