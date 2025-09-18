#!/usr/bin/env python3
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.models import db, User

def create_admin_user():
    app = create_app()
    with app.app_context():
        try:
            # Check if admin already exists
            admin_user = User.query.filter_by(role='admin').first()
            if admin_user:
                print(f"✅ Admin user already exists: {admin_user.username}")
                return
            
            # Create admin user
            admin = User(
                username='admin',
                email='admin@secureshare.com',
                role='admin'
            )
            admin.password = 'admin123'  # Change this password!
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Email: admin@secureshare.com") 
            print("   Password: admin123")
            print("   ⚠️  Please change the password after first login!")
            
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin_user()
