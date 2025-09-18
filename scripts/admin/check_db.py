#!/usr/bin/env python3
import sys
import os
# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.models import db, User

def check_users():
    app = create_app()
    with app.app_context():
        try:
            print("🔍 Checking database for users...")
            users = User.query.all()
            
            if not users:
                print("📭 No users found in database")
                print("ℹ️  Register a user through the web interface to see them here")
            else:
                print(f"👥 Found {len(users)} users:")
                for user in users:
                    print(f"  - {user.username} ({user.email}) - Role: {user.role}")
                    
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_users()
