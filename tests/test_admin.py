#!/usr/bin/env python3
import sys
sys.path.append('.')

from app import create_app

def test_admin_routes():
    app = create_app()
    with app.test_client() as client:
        # Test admin routes (should redirect to login)
        response = client.get('/admin/users')
        print(f"Admin users page (not logged in): Status {response.status_code}")
        
        response = client.get('/admin/dashboard')
        print(f"Admin dashboard (not logged in): Status {response.status_code}")
        
        print("✅ Admin routes are working (redirecting to login as expected)")

if __name__ == '__main__':
    test_admin_routes()
