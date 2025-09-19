#!/usr/bin/env python3
"""
User Database Management Script
Provides safe options to clear users from the SecureShare database
"""

import sys
import os
sys.path.append('.')

from app import create_app
from app.models import db, User

def view_all_users():
    """Display all current users before deletion"""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        if not users:
            print("📭 No users found in the database.")
            return False
        
        print(f"👥 Current users in database ({len(users)} total):")
        print("-" * 60)
        for user in users:
            print(f"  ID: {user.id} | {user.username} ({user.email}) - Role: {user.role}")
        print("-" * 60)
        return True

def clear_all_users():
    """Clear all users from the database"""
    app = create_app()
    with app.app_context():
        try:
            # Count users before deletion
            user_count = User.query.count()
            
            if user_count == 0:
                print("📭 No users to delete.")
                return
            
            # Delete all users
            User.query.delete()
            db.session.commit()
            
            print(f"✅ Successfully deleted {user_count} user(s) from the database.")
            print("🔄 Database is now empty of users.")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error clearing users: {e}")

def clear_non_admin_users():
    """Clear only regular users, keep admin users"""
    app = create_app()
    with app.app_context():
        try:
            # Count regular users before deletion
            regular_users = User.query.filter_by(role='user').all()
            count = len(regular_users)
            
            if count == 0:
                print("📭 No regular users to delete.")
                return
            
            # Delete only regular users
            User.query.filter_by(role='user').delete()
            db.session.commit()
            
            print(f"✅ Successfully deleted {count} regular user(s).")
            
            # Show remaining admin users
            remaining_admins = User.query.filter_by(role='admin').all()
            if remaining_admins:
                print(f"👑 {len(remaining_admins)} admin user(s) preserved:")
                for admin in remaining_admins:
                    print(f"  - {admin.username} ({admin.email})")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error clearing regular users: {e}")

def clear_specific_user():
    """Clear a specific user by username"""
    app = create_app()
    with app.app_context():
        try:
            username = input("Enter username to delete: ").strip()
            if not username:
                print("❌ No username provided.")
                return
            
            user = User.query.filter_by(username=username).first()
            if not user:
                print(f"❌ User '{username}' not found.")
                return
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete user '{username}' ({user.email})? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("❌ Deletion cancelled.")
                return
            
            db.session.delete(user)
            db.session.commit()
            
            print(f"✅ Successfully deleted user '{username}'.")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error deleting user: {e}")

def interactive_menu():
    """Interactive menu for user management"""
    while True:
        print("\n" + "="*50)
        print("🗃️  SecureShare User Database Management")
        print("="*50)
        
        # Show current users first
        has_users = view_all_users()
        
        if not has_users:
            print("\n💡 No users to manage. Exiting...")
            break
        
        print("\nOptions:")
        print("1. 🗑️  Clear ALL users (including admins)")
        print("2. 👥 Clear only regular users (keep admins)")
        print("3. 🎯 Delete specific user")
        print("4. 🔄 Refresh user list")
        print("5. ❌ Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n⚠️  WARNING: This will delete ALL users including admins!")
            confirm = input("Type 'DELETE ALL' to confirm: ").strip()
            if confirm == 'DELETE ALL':
                clear_all_users()
            else:
                print("❌ Operation cancelled.")
        
        elif choice == '2':
            print("\n📝 This will delete regular users but keep admin users.")
            confirm = input("Type 'yes' to confirm: ").strip().lower()
            if confirm == 'yes':
                clear_non_admin_users()
            else:
                print("❌ Operation cancelled.")
        
        elif choice == '3':
            clear_specific_user()
        
        elif choice == '4':
            continue  # Will refresh the user list
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    print("🔧 SecureShare User Database Management Tool")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'clear-all':
            print("⚠️  Clearing ALL users...")
            if view_all_users():
                confirm = input("Type 'DELETE ALL' to confirm: ").strip()
                if confirm == 'DELETE ALL':
                    clear_all_users()
                else:
                    print("❌ Operation cancelled.")
        
        elif command == 'clear-users':
            print("📝 Clearing regular users (keeping admins)...")
            if view_all_users():
                confirm = input("Type 'yes' to confirm: ").strip().lower()
                if confirm == 'yes':
                    clear_non_admin_users()
                else:
                    print("❌ Operation cancelled.")
        
        elif command == 'view':
            view_all_users()
        
        else:
            print("❌ Unknown command. Available commands:")
            print("  python scripts/clear_users.py view         - View all users")
            print("  python scripts/clear_users.py clear-users  - Clear regular users")
            print("  python scripts/clear_users.py clear-all    - Clear ALL users")
            print("  python scripts/clear_users.py              - Interactive mode")
    
    else:
        # Interactive mode
        interactive_menu()
