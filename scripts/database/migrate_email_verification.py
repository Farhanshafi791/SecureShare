#!/usr/bin/env python3
"""
Database migration script to add email verification fields to User model
"""

import sys
import os

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, User

def migrate_database():
    """Add email verification fields to existing User model"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Starting database migration for email verification...")
            
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            if 'is_verified' not in columns:
                print("📝 Adding is_verified column...")
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT 0 NOT NULL"))
                    conn.commit()
            else:
                print("✅ is_verified column already exists")
            
            if 'verification_token' not in columns:
                print("📝 Adding verification_token column...")
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE user ADD COLUMN verification_token VARCHAR(100)"))
                    conn.commit()
            else:
                print("✅ verification_token column already exists")
            
            # Update existing users to be verified (for backward compatibility)
            print("🔄 Updating existing users to verified status...")
            with db.engine.connect() as conn:
                conn.execute(db.text("UPDATE user SET is_verified = 1 WHERE is_verified = 0"))
                conn.commit()
            
            print("✅ Database migration completed successfully!")
            print("📊 All existing users have been marked as verified")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Email Verification Database Migration")
    print("=" * 60)
    
    if migrate_database():
        print("\n🎉 Migration completed successfully!")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)
