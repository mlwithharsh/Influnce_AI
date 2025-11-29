# InfluenceAI - Social Media Analytics Platform

A modern, AI-powered social media analytics platform that helps influencers track and optimize their content across Instagram, Twitter, and YouTube.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [OAuth Setup](#oauth-setup)
- [API Documentation](#api-documentation)
- [Development Guide](#development-guide)
- [Deployment](#deployment)

## ✨ Features

### Authentication
- 🔐 User registration and login with JWT
- 🔗 OAuth 2.0 integration for Instagram, Twitter, and YouTube
- 🛡️ Secure password hashing with bcrypt
- 💾 Persistent sessions

### Analytics Dashboard
- 📊 Real-time statistics across all platforms
- 📈 Engagement metrics and growth tracking
- 🎯 Platform-specific performance insights
- 🤖 AI-powered recommendations

### Social Media Integration
- 📸 Instagram: Posts, insights, profile data
- 🐦 Twitter: Tweets, metrics, profile info
- 🎥 YouTube: Videos, channel analytics, statistics

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **Redis** - Caching layer
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **PyJWT** - JWT authentication
- **HTTPX** - Async HTTP client for OAuth

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Zustand** - State management
- **React Router** - Client-side routing

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker Desktop
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Influnce_AI
   ```

2. **Start Docker services**
   ```bash
   docker-compose up -d
   ```
   This starts PostgreSQL and Redis containers.

3. **Backend Setup**
   ```bash
   # Install Python dependencies
   pip install -r backend/requirements.txt

   # Run database migrations
   python -m alembic upgrade head

   # Start the backend server
   python -m uvicorn backend.app.main:app --reload
   ```
   Backend runs on: http://localhost:8000

4. **Frontend Setup**
   ```bash
   # Install Node dependencies
   npm install

   # Start the development server
   npm run dev
   ```
   Frontend runs on: http://localhost:5173

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
Influnce_AI/
├── backend/                    # Backend API
│   ├── app/
│   │   ├── core/              # Core utilities
│   │   │   ├── auth.py        # JWT and password utilities
│   │   │   ├── database.py    # Database connection
│   │   │   └── redis.py       # Redis client
│   │   ├── db/                # Database layer
│   │   │   ├── models.py      # SQLAlchemy models
│   │   │   └── crud.py        # Database operations
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py        # Authentication & OAuth
│   │   │   └── social.py      # Social media analytics
│   │   └── main.py            # FastAPI application
│   ├── etl/                   # ETL pipelines (optional)
│   ├── db/init/               # Database initialization scripts
│   └── requirements.txt       # Python dependencies
├── src/                       # Frontend application
│   ├── pages/                 # React pages
│   │   ├── Login.tsx          # Login/Register page
│   │   ├── Dashboard.tsx      # Main dashboard
│   │   └── OAuthCallback.tsx  # OAuth callback handler
│   ├── stores/                # State management
│   │   └── authStore.ts       # Authentication store
│   ├── components/            # Reusable components
│   └── App.tsx                # Main app with routing
├── alembic/                   # Database migrations
├── docker-compose.yml         # Docker services configuration
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🔑 OAuth Setup

To enable social media connections, you need to obtain OAuth credentials from each platform.

### 1. Instagram (Facebook Developers)

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or select existing
3. Add "Instagram Basic Display" product
4. Configure OAuth redirect URI: `http://localhost:8000/auth/instagram/callback`
5. Copy your App ID and App Secret

### 2. Twitter/X (Twitter Developer Portal)

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Enable OAuth 2.0
4. Add callback URL: `http://localhost:8000/auth/twitter/callback`
5. Copy your Client ID and Client Secret

### 3. YouTube (Google Cloud Console)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3 and YouTube Analytics API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/auth/youtube/callback`
6. Copy your Client ID and Client Secret

### 4. Update Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```env
# Database
DATABASE_URL=postgresql+psycopg2://influnce:influnce_password@localhost:5432/influnce_ai

# Instagram OAuth
INSTAGRAM_APP_ID=your_instagram_app_id
INSTAGRAM_SECRET=your_instagram_secret
INSTAGRAM_REDIRECT_URI=http://localhost:8000/auth/instagram/callback

# Twitter OAuth
TWITTER_CLIENT_ID=your_twitter_client_id
TWITTER_CLIENT_SECRET=your_twitter_client_secret
TWITTER_REDIRECT_URI=http://localhost:8000/auth/twitter/callback

# YouTube OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/youtube/callback

# JWT Secret (generate a long random string)
JWT_SECRET=your_very_long_random_secret_key_here
```

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword"
}
```

### OAuth Endpoints

#### Get OAuth URL
```http
GET /auth/{platform}
# platform: instagram, twitter, or youtube
```

#### OAuth Callback (handled automatically)
```http
GET /auth/{platform}/callback?code=...
```

### Analytics Endpoints

#### Get Instagram Insights
```http
GET /social/instagram/insights?user_id=1
Authorization: Bearer {jwt_token}
```

#### Get Twitter Tweets
```http
GET /social/twitter/tweets?user_id=1
Authorization: Bearer {jwt_token}
```

#### Get YouTube Analytics
```http
GET /social/youtube/analytics?user_id=1
Authorization: Bearer {jwt_token}
```

#### Get Connected Accounts
```http
GET /social/connected-accounts?user_id=1
Authorization: Bearer {jwt_token}
```

For complete API documentation, visit: http://localhost:8000/docs

## 💻 Development Guide

### Database Migrations

Create a new migration:
```bash
python -m alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
python -m alembic upgrade head
```

Rollback migration:
```bash
python -m alembic downgrade -1
```

### Adding a New API Endpoint

1. Define the endpoint in `backend/app/routes/`
2. Add database operations in `backend/app/db/crud.py` if needed
3. Update models in `backend/app/db/models.py` if needed
4. Create and apply migrations

### Adding a New Frontend Page

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Update navigation if needed

### Code Style

- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: Use TypeScript strict mode
- **Comments**: Add comments for complex logic
- **Naming**: Use descriptive variable and function names

## 🚢 Deployment

### Backend Deployment

1. Set environment variables on your hosting platform
2. Update `DATABASE_URL` to production database
3. Update OAuth redirect URIs to production URLs
4. Run migrations: `python -m alembic upgrade head`
5. Start with: `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000`

### Frontend Deployment

1. Update API URL in `src/stores/authStore.ts`
2. Build: `npm run build`
3. Deploy `dist/` folder to hosting platform (Vercel, Netlify, etc.)
4. Update OAuth callback URLs to production domain

### Environment Variables for Production

```env
# Use strong, random values
JWT_SECRET=<long-random-string>

# Use production database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Update all redirect URIs to production domain
INSTAGRAM_REDIRECT_URI=https://yourdomain.com/auth/instagram/callback
TWITTER_REDIRECT_URI=https://yourdomain.com/auth/twitter/callback
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/youtube/callback
```

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use strong JWT secrets** - Generate with `openssl rand -hex 32`
3. **Enable HTTPS in production** - Required for OAuth
4. **Rotate OAuth tokens regularly** - Implement refresh token logic
5. **Validate all user inputs** - Use Pydantic models
6. **Rate limit API endpoints** - Prevent abuse

## 🐛 Troubleshooting

### Database Connection Failed
```bash
# Restart Docker containers
docker-compose restart

# Check if containers are running
docker ps
```

### OAuth Not Working
- Verify backend is running on port 8000
- Check OAuth credentials in `.env`
- Ensure callback URLs match exactly
- Check browser console for errors

### Frontend Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Migration Errors
```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
python -m alembic upgrade head
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📧 Support

For issues or questions:
- Check existing documentation
- Review code comments
- Open an issue on GitHub

---

Built with ❤️ using FastAPI and React
