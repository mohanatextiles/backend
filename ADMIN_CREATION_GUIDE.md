# 👤 Admin User Creation Guide

Complete guide to creating and managing admin users for Mohana Textiles.

---

## 🎯 Overview

Admin users have full access to:
- Product management (create, edit, delete)
- Category management
- Settings configuration
- Dashboard analytics

---

## 🚀 Method 1: Interactive Script (Recommended)

Use the interactive Python script for easy admin creation.

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Run the Script
```bash
python create_admin.py
```

### Step 3: Follow the Menu

You'll see:
```
=== Mohana Textiles Admin Management ===

1. Create new admin user
2. List all admin users
3. Exit

Choose an option (1-3):
```

### Step 4: Create Admin

1. Select option **1** (Create new admin user)
2. Enter email address
3. Enter password (hidden for security)
4. Confirm password
5. Done! ✅

### Example Session
```bash
$ python create_admin.py

=== Mohana Textiles Admin Management ===

1. Create new admin user
2. List all admin users
3. Exit

Choose an option (1-3): 1

Enter admin email: admin@mohanatextiles.com
Enter admin password: ••••••••••••
Confirm password: ••••••••••••

✅ Admin user created successfully!
Email: admin@mohanatextiles.com
```

---

## 🔧 Method 2: Environment Variables

Set admin credentials in environment variables (for first admin only).

### Local Development

Add to `backend/.env`:
```bash
ADMIN_EMAIL=admin@mohanatextiles.com
ADMIN_PASSWORD=YourSecurePassword123
```

### Production (Hugging Face)

Add to Hugging Face Space secrets:
```
ADMIN_EMAIL=admin@mohanatextiles.com
ADMIN_PASSWORD=YourSecurePassword123
```

**Note**: This creates the admin on first startup if it doesn't exist.

---

## 🌐 Method 3: API Endpoint (Production)

Create admin via API after deployment.

### Step 1: Get Token

First, login with environment-configured admin or use database.

### Step 2: Call API

```bash
curl -X POST "https://your-space.hf.space/api/auth/create-admin" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newadmin@mohanatextiles.com",
    "password": "SecurePassword123"
  }'
```

**Response**:
```json
{
  "email": "newadmin@mohanatextiles.com",
  "message": "Admin created successfully"
}
```

---

## 📋 Admin Management

### List All Admins

```bash
python create_admin.py
# Select option 2
```

This shows:
- All admin email addresses
- Total number of admins

### Reset Admin Password

Currently, to reset a password:

1. **Option A**: Delete admin from database and recreate
2. **Option B**: Manually update in database
3. **Option C**: Update ADMIN_PASSWORD in environment and restart

**Future Enhancement**: Password reset will be added to the script.

---

## 🔒 Security Best Practices

### Password Requirements

Use strong passwords with:
- ✅ At least 12 characters
- ✅ Mix of uppercase and lowercase
- ✅ Numbers
- ✅ Special characters
- ❌ No common words
- ❌ No personal information

### Example Strong Passwords
```
Tx$2024@MohanA!
SecureM0H#Textile
Admin@MT$2024!Pass
```

### Storage

- Passwords are hashed with SHA-256
- Never stored in plain text
- Environment variables kept secure
- Never commit passwords to Git

### Access Control

- ✅ Limit admin accounts (2-3 maximum)
- ✅ Use unique passwords per admin
- ✅ Change passwords periodically
- ✅ Remove unused admin accounts
- ❌ Don't share admin credentials
- ❌ Don't use same password across services

---

## 🐛 Troubleshooting

### Script Won't Run

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

**Problem**: `Database connection error`
```bash
# Solution: Check .env file
cat .env
# Verify DATABASE_URL is correct
```

### Password Issues

**Problem**: Password rejected during creation
- Ensure password meets requirements (8+ characters)
- Check for typos in password confirmation
- Avoid special characters that might cause issues

**Problem**: Can't login with created admin
```bash
# Verify admin exists
python create_admin.py
# Select option 2 to list admins
```

### Database Issues

**Problem**: "Admin already exists"
```bash
# Solution: Use a different email or delete existing admin
# To see existing admins:
python create_admin.py
# Select option 2
```

---

## 📝 Admin Creation Checklist

Before creating admin:

- [ ] Backend dependencies installed
- [ ] Database connection working
- [ ] `.env` file configured
- [ ] Strong password prepared
- [ ] Email address ready

After creating admin:

- [ ] Test login at `/admin/login`
- [ ] Verify dashboard access
- [ ] Test product creation
- [ ] Test category management
- [ ] Save credentials securely

---

## 🚀 Quick Commands Reference

```bash
# Create admin (interactive)
cd backend && python create_admin.py

# List admins
cd backend && python create_admin.py
# Then select option 2

# Check if admin exists (via Python)
cd backend && python -c "
from app.database import AsyncSessionLocal
from app.services.auth import AuthService
import asyncio

async def check():
    async with AsyncSessionLocal() as db:
        admin = await AuthService.get_admin_by_email(db, 'admin@mohanatextiles.com')
        print('Admin exists!' if admin else 'Admin not found')

asyncio.run(check())
"
```

---

## 📞 Need Help?

If you encounter issues:

1. **Check Logs**: Look for error messages
2. **Verify Database**: Ensure connection is working
3. **Check Environment**: Verify .env variables
4. **Test Connection**: Run `python migrate_db.py` to test DB

---

## 🎯 Production Deployment

For production admin creation:

1. **Before Deployment**:
   - Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in Hugging Face secrets
   - This creates first admin automatically

2. **After Deployment**:
   - Use API endpoint to create additional admins
   - Or SSH into container and run `create_admin.py`

3. **Best Practice**:
   - Create one admin via environment variables
   - Create additional admins via admin panel (after login)

---

## ✅ Success!

You now have admin access to:
- Dashboard: `/admin`
- Products: `/admin/products`
- Categories: `/admin/categories`
- Settings: `/admin/settings`

Happy managing! 🎉
