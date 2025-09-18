#!/usr/bin/env python3
"""
Database migration script for file functionality
Adds new File and AccessLog tables and updates User model relationships
"""

import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app
from app.models import db, User, File, AccessLog

def migrate_database():
    """Migrate the database to support file functionality"""
    print("SecureShare Database Migration")
    print("=" * 35)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables (this will create new ones and leave existing ones alone)
            print("Creating database tables...")
            db.create_all()
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Database tables: {', '.join(tables)}")
            
            # Check if File table has all required columns
            if 'file' in tables:
                file_columns = [col['name'] for col in inspector.get_columns('file')]
                required_columns = ['id', 'filename', 'original_filename', 'encrypted_path', 
                                  'file_size', 'mime_type', 'upload_time', 'owner_id', 
                                  'is_shared', 'download_count']
                
                missing_columns = [col for col in required_columns if col not in file_columns]
                if missing_columns:
                    print(f"⚠️  Missing File table columns: {missing_columns}")
                    print("You may need to delete the database and recreate it")
                else:
                    print("✅ File table has all required columns")
            
            # Check if AccessLog table has all required columns
            if 'access_log' in tables:
                log_columns = [col['name'] for col in inspector.get_columns('access_log')]
                required_log_columns = ['id', 'action', 'timestamp', 'user_id', 'file_id']
                
                missing_log_columns = [col for col in required_log_columns if col not in log_columns]
                if missing_log_columns:
                    print(f"⚠️  Missing AccessLog table columns: {missing_log_columns}")
                    print("You may need to delete the database and recreate it")
                else:
                    print("✅ AccessLog table has all required columns")
            
            # Create upload directory
            from config import Config
            upload_dir = Config.UPLOAD_FOLDER
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                print(f"✅ Created upload directory: {upload_dir}")
            else:
                print(f"✅ Upload directory exists: {upload_dir}")
            
            print("\n🎉 Database migration completed successfully!")
            print("\nYour SecureShare application is now ready for file upload and download functionality!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrate_database()
