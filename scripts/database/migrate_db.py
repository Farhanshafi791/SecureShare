#!/usr/bin/env python3
"""
Database migration script to update the User table schema
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.models import db

def migrate_database():
    """Recreate the database with the new schema"""
    app = create_app()
    
    with app.app_context():
        # Check if there's an existing database file
        db_file = os.path.join(app.instance_path, 'database.db')
        if os.path.exists(db_file):
            print(f"Found existing database at: {db_file}")
            backup_file = db_file + '.backup'
            try:
                os.rename(db_file, backup_file)
                print(f"Backed up existing database to: {backup_file}")
            except Exception as e:
                print(f"Warning: Could not backup database: {e}")
        
        # Drop all tables and recreate them
        print("Dropping all existing tables...")
        db.drop_all()
        
        print("Creating new tables with updated schema...")
        db.create_all()
        
        print("✅ Database migration completed successfully!")
        print("You can now run your application with the updated User model.")

if __name__ == '__main__':
    print("SecureShare Database Migration")
    print("=" * 40)
    migrate_database()
