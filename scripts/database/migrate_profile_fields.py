#!/usr/bin/env python3
"""
Migration script to add profile fields to the User model.
This script adds first_name, last_name, bio, timezone, and language fields to the User table.
"""

import os
import sys
from sqlalchemy import text

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def migrate_profile_fields():
    """Add profile fields to the User table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if columns already exist
            result = db.session.execute(text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result.fetchall()]
            
            # Add columns if they don't exist
            fields_to_add = [
                ('first_name', 'VARCHAR(50)'),
                ('last_name', 'VARCHAR(50)'),
                ('bio', 'TEXT'),
                ('timezone', 'VARCHAR(50)'),
                ('language', 'VARCHAR(10)')
            ]
            
            for field_name, field_type in fields_to_add:
                if field_name not in columns:
                    print(f"Adding column {field_name}...")
                    db.session.execute(text(f"ALTER TABLE user ADD COLUMN {field_name} {field_type}"))
                else:
                    print(f"Column {field_name} already exists, skipping...")
            
            db.session.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Migration failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    migrate_profile_fields()