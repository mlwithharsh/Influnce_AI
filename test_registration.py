import requests
import sys

API_URL = "http://127.0.0.1:8000"

def test_register():
    print(f"Testing registration against {API_URL}...")
    
    # Randomize email to avoid "already exists" error
    import random
    suffix = random.randint(1000, 9999)
    email = f"test_{suffix}@example.com"
    
    payload = {
        "username": f"user_{suffix}",
        "email": email,
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/register", json=payload)
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Response Text: {response.text}")
            
        if response.status_code == 200:
            print("✅ Registration Successful")
        else:
            print("❌ Registration Failed")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_register()
