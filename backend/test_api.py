#!/usr/bin/env python3

import asyncio
from fastapi.testclient import TestClient
from app.main import app
import json

def test_api():
    client = TestClient(app)
    
    print("🧪 Testing Template Sharing Platform API")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = client.get("/")
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test health endpoint
    try:
        response = client.get("/api/health")
        print(f"✅ Health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test user registration
    try:
        user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "role": "user"
        }
        response = client.post("/api/auth/register", json=user_data)
        print(f"✅ User registration: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ User registration failed: {e}")
    
    # Test admin registration
    try:
        admin_data = {
            "email": "admin@example.com",
            "username": "admin",
            "password": "adminpassword123",
            "role": "admin"
        }
        response = client.post("/api/auth/register", json=admin_data)
        print(f"✅ Admin registration: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Admin registration failed: {e}")
    
    # Test user login
    try:
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = client.post("/api/auth/login", json=login_data)
        print(f"✅ User login: {response.status_code}")
        if response.status_code == 200:
            user_token = response.json()["access_token"]
            print(f"   User token: {user_token[:50]}...")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ User login failed: {e}")
        user_token = None
    
    # Test admin login
    try:
        login_data = {
            "email": "admin@example.com",
            "password": "adminpassword123"
        }
        response = client.post("/api/auth/login", json=login_data)
        print(f"✅ Admin login: {response.status_code}")
        if response.status_code == 200:
            admin_token = response.json()["access_token"]
            print(f"   Admin token: {admin_token[:50]}...")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Admin login failed: {e}")
        admin_token = None
    
    # Test templates endpoint (should require authentication)
    try:
        response = client.get("/api/templates")
        print(f"✅ Templates (no auth): {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Templates (no auth) failed: {e}")
    
    # Test templates with user token
    if user_token:
        try:
            headers = {"Authorization": f"Bearer {user_token}"}
            response = client.get("/api/templates", headers=headers)
            print(f"✅ Templates (user auth): {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"❌ Templates (user auth) failed: {e}")
    
    print("\n🎉 API test completed!")

if __name__ == "__main__":
    test_api()
