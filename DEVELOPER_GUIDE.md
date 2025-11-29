# Developer Guide - InfluenceAI

This guide will help you understand and work with the InfluenceAI codebase.

## 📂 Code Organization

### Backend Structure

```
backend/
├── app/
│   ├── core/              # Core utilities and configuration
│   │   ├── auth.py        # JWT and password utilities
│   │   ├── database.py    # Database connection and session
│   │   └── redis.py       # Redis client configuration
│   ├── db/                # Database layer
│   │   ├── models.py      # SQLAlchemy ORM models
│   │   └── crud.py        # Database CRUD operations
│   └── routes/            # API endpoints
│       ├── auth.py        # Authentication and OAuth routes
│       └── social.py      # Social media analytics routes
```

### Frontend Structure

```
src/
├── pages/                 # React page components
│   ├── Login.tsx          # Login/Register page
│   ├── Dashboard.tsx      # Main dashboard with OAuth
│   └── OAuthCallback.tsx  # OAuth callback handler
├── stores/                # Zustand state management
│   └── authStore.ts       # Authentication state
└── App.tsx                # Main app with routing
```

## 🔧 Key Concepts

### 1. Authentication Flow

**Registration:**
1. User submits username, email, password
2. Backend hashes password with bcrypt
3. User record created in database
4. JWT token generated and returned
5. Frontend stores token in Zustand + localStorage

**Login:**
1. User submits email, password
2. Backend verifies password hash
3. JWT token generated and returned
4. Frontend stores token and fetches connected accounts

### 2. OAuth Flow

**Connection Process:**
1. User clicks "Connect" on platform card
2. Frontend redirects to `/auth/{platform}`
3. Backend generates OAuth URL and redirects
4. User authorizes on platform's page
5. Platform redirects to `/auth/{platform}/callback`
6. Backend exchanges code for access token
7. Token stored in `social_accounts` table
8. User redirected back to dashboard

**Important Files:**
- Backend: `backend/app/routes/auth.py` (OAuth endpoints)
- Frontend: `src/pages/Dashboard.tsx` (Connect buttons)
- Frontend: `src/pages/OAuthCallback.tsx` (Callback handler)

### 3. Database Models

**User Model:**
- Stores user credentials
- One-to-many relationship with SocialAccount

**SocialAccount Model:**
- Stores OAuth tokens per platform
- Unique constraint: one account per platform per user
- Contains: platform, account_id, access_token

**PostAnalytics Model:**
- Stores post metrics (likes, comments, views)
- Linked to SocialAccount

## 🛠️ Common Tasks

### Adding a New OAuth Platform

1. **Add environment variables** (`.env`):
   ```env
   NEWPLATFORM_CLIENT_ID=xxx
   NEWPLATFORM_CLIENT_SECRET=xxx
   NEWPLATFORM_REDIRECT_URI=http://localhost:8000/auth/newplatform/callback
   ```

2. **Add OAuth routes** (`backend/app/routes/auth.py`):
   ```python
   @router.get('/newplatform')
   def newplatform_auth():
       # Generate OAuth URL
       return {"auth_url": oauth_url}
   
   @router.get('/newplatform/callback')
   async def newplatform_callback(code: str, db: Session = Depends(get_db)):
       # Exchange code for token
       # Store in database
       return {"message": "Connected"}
   ```

3. **Add analytics routes** (`backend/app/routes/social.py`):
   ```python
   @router.get('/newplatform/stats')
   async def get_newplatform_stats(user_id: int, db: Session = Depends(get_db)):
       token = get_token_from_db(db, user_id, "newplatform")
       # Fetch and return data
   ```

4. **Update frontend** (`src/pages/Dashboard.tsx`):
   - Add platform to connection cards array
   - Add icon and color scheme

### Adding a New API Endpoint

1. **Define route** in appropriate file:
   ```python
   @router.get('/new-endpoint')
   async def new_endpoint(param: str):
       # Your logic here
       return {"result": data}
   ```

2. **Add database operations** if needed (`backend/app/db/crud.py`):
   ```python
   def get_something(db: Session, id: int):
       return db.query(models.Something).filter(...).first()
   ```

3. **Update models** if needed (`backend/app/db/models.py`):
   ```python
   class NewModel(Base):
       __tablename__ = "new_table"
       id = Column(Integer, primary_key=True)
       # ... other fields
   ```

4. **Create migration**:
   ```bash
   python -m alembic revision --autogenerate -m "Add new table"
   python -m alembic upgrade head
   ```

### Adding a New Frontend Page

1. **Create page component** (`src/pages/NewPage.tsx`):
   ```tsx
   export default function NewPage() {
       return <div>New Page Content</div>;
   }
   ```

2. **Add route** (`src/App.tsx`):
   ```tsx
   <Route
       path="/new-page"
       element={
           <ProtectedRoute>
               <NewPage />
           </ProtectedRoute>
       }
   />
   ```

3. **Add navigation** if needed in your layout component

## 🔍 Debugging Tips

### Backend Debugging

**Check logs:**
```bash
# Backend logs show in terminal where uvicorn is running
# Look for error messages and stack traces
```

**Test API directly:**
- Visit http://localhost:8000/docs
- Use the interactive Swagger UI
- Test endpoints without frontend

**Database inspection:**
```bash
# Connect to PostgreSQL
docker exec -it influnce_ai_postgres psql -U influnce -d influnce_ai

# List tables
\dt

# Query data
SELECT * FROM users;
SELECT * FROM social_accounts;
```

### Frontend Debugging

**Check browser console:**
- Open DevTools (F12)
- Look for network errors
- Check console logs

**Inspect state:**
```tsx
// Add temporary logging
const { user, token } = useAuthStore();
console.log('User:', user);
console.log('Token:', token);
```

**Check localStorage:**
- DevTools → Application → Local Storage
- Look for `auth-storage` key

## 📝 Code Style Guidelines

### Backend (Python)

```python
# Use type hints
def get_user(db: Session, user_id: int) -> User:
    pass

# Add docstrings
def create_user(db: Session, email: str) -> User:
    """
    Create a new user
    
    Args:
        db: Database session
        email: User's email
        
    Returns:
        Created User object
    """
    pass

# Use descriptive names
user_email = "test@example.com"  # Good
e = "test@example.com"  # Bad
```

### Frontend (TypeScript)

```tsx
// Use TypeScript interfaces
interface User {
    id: number;
    email: string;
}

// Add JSDoc comments for complex functions
/**
 * Fetch user analytics data
 * @param userId - The user's ID
 * @returns Promise with analytics data
 */
async function fetchAnalytics(userId: number): Promise<Analytics> {
    // ...
}

// Use descriptive component names
function UserDashboard() {}  // Good
function Comp1() {}  // Bad
```

## 🧪 Testing

### Manual Testing Checklist

**Authentication:**
- [ ] Register new user
- [ ] Login with correct credentials
- [ ] Login with wrong credentials (should fail)
- [ ] Logout
- [ ] Session persists after page refresh

**OAuth:**
- [ ] Connect Instagram account
- [ ] Connect Twitter account
- [ ] Connect YouTube account
- [ ] Disconnect account
- [ ] Reconnect same account (should update token)

**API:**
- [ ] Fetch Instagram insights
- [ ] Fetch Twitter tweets
- [ ] Fetch YouTube analytics
- [ ] Get connected accounts list

## 🚀 Deployment Checklist

**Before deploying:**
- [ ] Update all OAuth redirect URIs to production domain
- [ ] Generate strong JWT_SECRET
- [ ] Use production database
- [ ] Enable HTTPS
- [ ] Update CORS settings
- [ ] Set proper environment variables
- [ ] Test all OAuth flows in production
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Add error monitoring (Sentry, etc.)

## 🐛 Common Issues

**"Database connection failed"**
- Check if Docker containers are running: `docker ps`
- Restart containers: `docker-compose restart`

**"OAuth redirect mismatch"**
- Verify callback URLs match exactly in OAuth app settings
- Check for trailing slashes
- Ensure http vs https matches

**"Token expired"**
- Tokens expire after 24 hours
- User needs to login again
- Consider implementing refresh tokens

**"CORS error"**
- Backend needs to allow frontend origin
- Check FastAPI CORS middleware configuration

## 📚 Resources

**Backend:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

**Frontend:**
- [React Documentation](https://react.dev/)
- [Zustand State Management](https://zustand-demo.pmnd.rs/)
- [Tailwind CSS](https://tailwindcss.com/)

**OAuth:**
- [Instagram API](https://developers.facebook.com/docs/instagram-basic-display-api)
- [Twitter API](https://developer.twitter.com/en/docs/authentication/oauth-2-0)
- [YouTube API](https://developers.google.com/youtube/v3)

## 💡 Best Practices

1. **Always use environment variables** for secrets
2. **Never commit `.env` file** to version control
3. **Add comments** for complex logic
4. **Use type hints** in Python
5. **Use TypeScript** instead of JavaScript
6. **Handle errors gracefully** with try-catch
7. **Validate user input** on both frontend and backend
8. **Use database transactions** for multi-step operations
9. **Test OAuth flows** thoroughly before deploying
10. **Keep dependencies updated** regularly

---

Happy coding! If you have questions, check the inline code comments or README.md.
