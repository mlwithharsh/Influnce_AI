"""
Health Check Script for InfluenceAI

This script verifies that all components are properly configured.
"""

import sys
import os

print("🔍 InfluenceAI Health Check\n")
print("=" * 50)

# Check 1: Database Connection
print("\n1️⃣  Checking Database Connection...")
try:
    from sqlalchemy import create_engine
    from backend.app.core.database import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("   ✅ Database connection successful")
except Exception as e:
    print(f"   ❌ Database connection failed: {e}")
    sys.exit(1)

# Check 2: Database Schema
print("\n2️⃣  Checking Database Schema...")
try:
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    required_tables = ['users', 'social_accounts', 'post_analytics', 'trends']
    
    for table in required_tables:
        if table in tables:
            print(f"   ✅ Table '{table}' exists")
        else:
            print(f"   ❌ Table '{table}' missing")
    
    # Check social_accounts columns
    columns = [c['name'] for c in inspector.get_columns('social_accounts')]
    if 'refresh_token' in columns and 'expires_at' in columns:
        print("   ✅ New OAuth columns (refresh_token, expires_at) present")
    else:
        print("   ❌ OAuth columns missing - run migrations")
except Exception as e:
    print(f"   ❌ Schema check failed: {e}")

# Check 3: Environment Variables
print("\n3️⃣  Checking Environment Variables...")
required_vars = [
    'GOOGLE_CLIENT_ID',
    'GOOGLE_CLIENT_SECRET',
    'GOOGLE_REDIRECT_URI',
    'JWT_SECRET'
]

for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"   ✅ {var} is set")
    else:
        print(f"   ⚠️  {var} is not set")

# Check 4: Dependencies
print("\n4️⃣  Checking Python Dependencies...")
try:
    import fastapi
    print(f"   ✅ FastAPI {fastapi.__version__}")
except ImportError:
    print("   ❌ FastAPI not installed")

try:
    import google_auth_oauthlib
    print(f"   ✅ google-auth-oauthlib installed")
except ImportError:
    print("   ❌ google-auth-oauthlib not installed - run: pip install google-auth-oauthlib")

try:
    import httpx
    print(f"   ✅ httpx installed")
except ImportError:
    print("   ❌ httpx not installed")

# Check 5: Backend Routes
print("\n5️⃣  Checking Backend Routes...")
try:
    from backend.app.routes import auth
    print("   ✅ Auth routes loaded")
    
    # Check if YouTube route exists
    routes = [route.path for route in auth.router.routes]
    if '/youtube' in routes:
        print("   ✅ YouTube OAuth route exists")
    else:
        print("   ❌ YouTube OAuth route missing")
except Exception as e:
    print(f"   ❌ Route check failed: {e}")

print("\n" + "=" * 50)
print("✅ Health check complete!\n")
print("Next steps:")
print("  1. Start backend: python -m uvicorn backend.app.main:app --reload")
print("  2. Start frontend: npm run dev")
print("  3. Visit: http://localhost:5173")
