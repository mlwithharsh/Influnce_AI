from sqlalchemy import create_engine, text
from backend.app.core.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT platform, account_id, refresh_token, expires_at FROM social_accounts WHERE platform='youtube'"))
    rows = result.fetchall()
    
    if rows:
        print("✅ YouTube tokens found in database:")
        for row in rows:
            print(f"  Platform: {row[0]}")
            print(f"  Account ID: {row[1]}")
            print(f"  Refresh Token: {row[2][:20]}..." if row[2] else "  Refresh Token: None")
            print(f"  Expires At: {row[3]}")
    else:
        print("❌ No YouTube tokens found. You need to connect your YouTube account first.")
