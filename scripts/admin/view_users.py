#!/usr/bin/env python3
"""
Database viewer script to see all users in the SecureShare database
"""

import os
import sys
sys.path.append('.')

from app import create_app
from app.models import db, User
from datetime import datetime

def view_all_users():
    """Display all users in the database"""
    app = create_app()
    
    with app.app_context():
        try:
            users = User.query.all()
            
            if not users:
                print("📭 No users found in the database.")
                print("Register some users first using the web interface.")
                return
            
            print(f"👥 Found {len(users)} user(s) in the database:")
            print("=" * 80)
            print(f"{'ID':<4} {'Username':<20} {'Email':<30} {'Role':<10} {'Created':<20}")
            print("-" * 80)
            
            for user in users:
                created_date = user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'N/A'
                print(f"{user.id:<4} {user.username:<20} {user.email:<30} {user.role:<10} {created_date:<20}")
            
            print("-" * 80)
            print(f"Total users: {len(users)}")
            
        except Exception as e:
            print(f"❌ Error viewing users: {e}")

def view_user_details(user_id):
    """Display detailed information for a specific user"""
    app = create_app()
    
    with app.app_context():
        try:
            user = User.query.get(user_id)
            
            if not user:
                print(f"❌ User with ID {user_id} not found.")
                return
            
            print(f"👤 User Details:")
            print("=" * 40)
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Created: {user.created_at}")
            print(f"Password Hash: {user.password_hash[:20]}..." if user.password_hash else "No password")
            
        except Exception as e:
            print(f"❌ Error viewing user details: {e}")

def search_users(search_term):
    """Search users by username or email"""
    app = create_app()
    
    with app.app_context():
        try:
            users = User.query.filter(
                (User.username.contains(search_term)) | 
                (User.email.contains(search_term))
            ).all()
            
            if not users:
                print(f"🔍 No users found matching '{search_term}'")
                return
            
            print(f"🔍 Found {len(users)} user(s) matching '{search_term}':")
            print("-" * 60)
            
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}")
            
        except Exception as e:
            print(f"❌ Error searching users: {e}")

if __name__ == '__main__':
    print("SecureShare Database User Viewer")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "details" and len(sys.argv) > 2:
            user_id = int(sys.argv[2])
            view_user_details(user_id)
        elif command == "search" and len(sys.argv) > 2:
            search_term = sys.argv[2]
            search_users(search_term)
        else:
            print("Usage:")
            print("  python view_users.py                    - View all users")
            print("  python view_users.py details <user_id>  - View user details")
            print("  python view_users.py search <term>      - Search users")
    else:
        view_all_users()
