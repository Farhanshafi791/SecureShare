#!/usr/bin/env python3
"""
Database Migration Script: Add ContactMessage table for Support System
This script adds the contact_message table to support the new Support System feature.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.contact_message import ContactMessage

def migrate_add_contact_message():
    """Add ContactMessage table to the database"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create the table
            db.create_all()
            print("✅ ContactMessage table created successfully")
            
            # Verify the table exists
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'contact_message' in tables:
                print("✅ Verified: contact_message table exists in database")
                
                # Show table structure
                columns = inspector.get_columns('contact_message')
                print("\n📋 Table structure:")
                for column in columns:
                    print(f"  - {column['name']}: {column['type']}")
                
                return True
            else:
                print("❌ Error: contact_message table was not created")
                return False
                
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False

if __name__ == '__main__':
    print("🔄 Starting ContactMessage table migration...")
    success = migrate_add_contact_message()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("📝 The Support System is now ready to use.")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
