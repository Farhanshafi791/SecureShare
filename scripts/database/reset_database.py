#!/usr/bin/env python3
"""
Database Reset Script
Completely resets the SecureShare database (drops and recreates all tables)
"""

import sys
import os
# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.models import db

def reset_database():
    """Drop all tables and recreate them (fresh start)"""
    app = create_app()
    with app.app_context():
        try:
            print("🗑️  Dropping all database tables...")
            db.drop_all()
            
            print("🔨 Creating fresh database tables...")
            db.create_all()
            
            print("✅ Database has been completely reset!")
            print("💡 All tables are now empty and ready for fresh data.")
            
        except Exception as e:
            print(f"❌ Error resetting database: {e}")

def backup_database():
    """Create a backup of the current database"""
    import shutil
    from datetime import datetime
    
    try:
        db_path = "instance/site.db"
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"instance/site_backup_{timestamp}.db"
            shutil.copy2(db_path, backup_path)
            print(f"✅ Database backed up to: {backup_path}")
            return backup_path
        else:
            print("📭 No database file found to backup.")
            return None
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

if __name__ == '__main__':
    print("🔄 SecureShare Database Reset Tool")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        # Force reset without confirmation
        print("⚠️  Force reset mode - no confirmation required")
        backup_database()
        reset_database()
    else:
        # Interactive mode with confirmation
        print("⚠️  WARNING: This will completely reset your database!")
        print("   • All users will be deleted")
        print("   • All files will be deleted") 
        print("   • All access logs will be deleted")
        print("   • This action cannot be undone!")
        
        # Offer backup
        backup_choice = input("\n💾 Do you want to create a backup first? (y/n): ").strip().lower()
        if backup_choice == 'y':
            backup_path = backup_database()
            if backup_path:
                print(f"📁 Backup created: {backup_path}")
        
        # Confirm reset
        print("\n🔄 Ready to reset database...")
        confirm = input("Type 'RESET DATABASE' to confirm: ").strip()
        
        if confirm == 'RESET DATABASE':
            reset_database()
        else:
            print("❌ Database reset cancelled.")
            print("💡 Your data is safe!")
