# 🏪 Mohana Textiles - Backend API

FastAPI backend for Mohana Textiles e-commerce platform.

## 🚀 Tech Stack

- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL (via Neon)
- **ORM**: SQLAlchemy 2.0 (async)
- **Python**: 3.11+
- **Authentication**: Token-based auth
- **Image Storage**: Google Drive

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Neon recommended)
- Google Drive folder for images

## 🔧 Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd mohana-textiles-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Database - Get from https://neon.tech
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require

# Google Drive
GOOGLE_DRIVE_FOLDER_URL=https://drive.google.com/drive/folders/YOUR_FOLDER_ID

# Optional - AI Features
OPENROUTER_API_KEY=your-api-key

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

### 5. Initialize Database

```bash
python migrate_db.py
```

### 6. Create Admin User

```bash
python create_admin.py
```

Follow the interactive prompts to create your admin account.

## 🏃 Running Locally

### Development Server

```bash
python run.py
```

API will be available at: http://localhost:8000

### API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## 📁 Project Structure

```
mohana-textiles-backend/
├── app/
│   ├── models/          # Database models
│   ├── routers/         # API endpoints
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── Dockerfile           # Docker configuration
├── app.yaml            # Hugging Face config
├── requirements.txt    # Python dependencies
├── run.py              # Development server
├── run_production.py   # Production server
├── migrate_db.py       # Database migration
├── create_admin.py     # Admin creation tool
└── .env                # Environment variables
```

## 🔐 Admin Management

### Create Admin User

```bash
python create_admin.py
```

Select option 1, enter email and password.

### List Admin Users

```bash
python create_admin.py
```

Select option 2 to view all admin accounts.

## 🚀 Deployment (Hugging Face Spaces)

### 1. Create Hugging Face Space

- Go to https://huggingface.co/spaces
- Create new Space with **Docker SDK**
- Name: `mohana-textiles-backend`

### 2. Upload Files

Upload all files from this repository to your Space.

### 3. Configure Secrets

In Space Settings > Repository secrets, add:

```
DATABASE_URL=postgresql+asyncpg://...?ssl=require
GOOGLE_DRIVE_FOLDER_URL=https://drive.google.com/drive/folders/...
CORS_ORIGINS=https://your-frontend.vercel.app
FRONTEND_URL=https://your-frontend.vercel.app
ENVIRONMENT=production
OPENROUTER_API_KEY=your-key (optional)
```

### 4. Deploy

Space will automatically build and deploy.

Your API will be at: `https://your-username-mohana-textiles-backend.hf.space`

## 📊 API Endpoints

### Public Endpoints

- `GET /` - Health check
- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product details
- `GET /api/categories` - List categories
- `GET /api/settings` - Get settings

### Admin Endpoints (Requires Authentication)

- `POST /api/auth/login` - Admin login
- `POST /api/auth/create-admin` - Create admin (admin only)
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product
- `POST /api/categories` - Create category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

## 🛠️ Development

### Database Migration

When you update models:

```bash
python migrate_db.py
```

**Warning**: This drops all tables and recreates them.

### Testing API

Use the interactive docs at `/docs` or use curl:

```bash
# Health check
curl http://localhost:8000/

# Get products
curl http://localhost:8000/api/products

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'
```

## 🐛 Troubleshooting

### Database Connection Error

- Verify `DATABASE_URL` format
- Ensure `?ssl=require` is included
- Check database is active in Neon dashboard

### CORS Errors

- Add frontend URL to `CORS_ORIGINS`
- Include protocol (http:// or https://)
- Restart server after changes

### Module Not Found

```bash
pip install -r requirements.txt
```

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `GOOGLE_DRIVE_FOLDER_URL` | Yes | Public Google Drive folder URL |
| `CORS_ORIGINS` | Yes | Allowed frontend origins |
| `FRONTEND_URL` | Yes | Frontend URL |
| `ENVIRONMENT` | Yes | `development` or `production` |
| `OPENROUTER_API_KEY` | No | For AI features |

## 🔒 Security

- Never commit `.env` files
- Use strong admin passwords
- Enable SSL for database connections
- Keep dependencies updated
- Use environment secrets in production

## 📞 Support

For issues or questions:
- Check API docs at `/docs`
- Review logs for error messages
- Verify environment variables
- Test database connection

## 📄 License

MIT License

---

**Built with ❤️ for Mohana Textiles**
