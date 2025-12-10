import requests
import json

# Test registration endpoint
url = "http://localhost:8000/auth/register"
data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

print("Testing registration endpoint...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print()

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✅ Registration successful!")
    else:
        print(f"\n❌ Registration failed: {response.json()}")
except Exception as e:
    print(f"\n❌ Error: {e}")
