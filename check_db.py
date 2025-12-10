from sqlalchemy import create_engine, text
from backend.app.core.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

print("Checking database tables and structure...\n")

with engine.connect() as conn:
    # Check if users table exists
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
    tables = [row[0] for row in result.fetchall()]
    
    print("📋 Available tables:")
    for table in tables:
        print(f"  - {table}")
    
    if 'users' in tables:
        print("\n✅ Users table exists")
        
        # Check users table structure
        result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='users'"))
        print("\n📊 Users table columns:")
        for row in result.fetchall():
            print(f"  - {row[0]}: {row[1]}")
        
        # Check if there are any users
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.fetchone()[0]
        print(f"\n👥 Total users in database: {count}")
    else:
        print("\n❌ Users table does not exist!")
        print("Run: python -m alembic upgrade head")
