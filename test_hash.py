from backend.app.core.auth import hash_password, verify_password

print("Testing password hashing...")

try:
    password = "password123"
    print(f"Original password: {password}")
    
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
    
    is_valid = verify_password(password, hashed)
    print(f"Verification result: {is_valid}")
    
    if is_valid:
        print("\n✅ Password hashing works correctly!")
    else:
        print("\n❌ Password verification failed!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
