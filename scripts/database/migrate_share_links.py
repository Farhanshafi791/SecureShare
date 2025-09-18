#!/usr/bin/env python3
"""
Database migration script to add share_token column to File model
Run this script to update your existing database with the new sharing functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db

def migrate_database():
    """Add share_token column to existing File table"""
    
    app = create_app()
    
    with app.app_context():
        print("🔄 Starting database migration...")
        
        try:
            # Check if the column already exists by trying to query it
            try:
                result = db.session.execute("SELECT share_token FROM file LIMIT 1")
                print("ℹ️  share_token column already exists")
            except:
                print("➕ Adding share_token column to File table...")
                
                # Add the new column using raw SQL
                db.session.execute(
                    "ALTER TABLE file ADD COLUMN share_token VARCHAR(64)"
                )
                db.session.commit()
                
                print("✅ Successfully added share_token column")
            
            print("🎉 Database migration completed successfully!")
            print("\n📋 Next steps:")
            print("   1. Restart your Flask application")
            print("   2. Users can now generate secure share links for their files")
            print("   3. Share links work without requiring login")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    success = migrate_database()
    if not success:
        sys.exit(1)
