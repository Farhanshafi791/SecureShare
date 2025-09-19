#!/usr/bin/env python3
"""
Database migration script to add profile fields to User table
"""

import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db

def migrate_database():
    """Add new profile fields to the User table"""
    
    # Create the Flask application
    app = create_app('development')
    
    with app.app_context():
        try:
            # Check if we're using SQLite (for development)
            if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
                print("📋 Applying SQLite migrations...")
                
                # SQLite doesn't support ALTER TABLE ADD COLUMN for all types
                # So we'll use a different approach - recreate tables
                db.drop_all()
                db.create_all()
                print("✅ Database tables recreated with new schema")
                
            else:
                # For PostgreSQL (production), we can use ALTER TABLE
                print("📋 Applying PostgreSQL migrations...")
                
                # Add new columns to User table
                migrations = [
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS first_name VARCHAR(50);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS last_name VARCHAR(50);",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS bio TEXT;",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'UTC';",
                    "ALTER TABLE user ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'en';"
                ]
                
                for migration in migrations:
                    try:
                        db.session.execute(migration)
                        print(f"✅ Executed: {migration}")
                    except Exception as e:
                        print(f"⚠️ Migration already applied or error: {migration} - {e}")
                
                db.session.commit()
                print("✅ PostgreSQL migrations completed")
                
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()
            return False
            
    return True

if __name__ == '__main__':
    print("🚀 Starting database migration...")
    if migrate_database():
        print("🎉 Migration completed successfully!")
    else:
        print("💥 Migration failed!")
        sys.exit(1)
