#!/usr/bin/env python3
"""
Check database schema and share tokens
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, File

def check_database():
    """Check the database schema and existing data"""
    
    print("🚀 Starting database check...")
    app = create_app()
    print("✅ App created")
    
    with app.app_context():
        print("🔍 Checking database schema...")
        
        try:
            # Check if we can query share_token
            files = File.query.all()
            print(f"📁 Found {len(files)} files in database")
            
            for file in files:
                print(f"   File ID {file.id}: {file.original_filename}")
                print(f"   - Shared: {file.is_shared}")
                try:
                    print(f"   - Share token: {file.share_token}")
                except Exception as token_error:
                    print(f"   - Share token error: {token_error}")
                print()
                
        except Exception as e:
            print(f"❌ Error querying database: {e}")
            
            # Try to see the schema
            try:
                result = db.session.execute("PRAGMA table_info(file)")
                columns = result.fetchall()
                print("📋 Current file table schema:")
                for col in columns:
                    print(f"   {col}")
            except Exception as schema_error:
                print(f"❌ Could not get schema: {schema_error}")

if __name__ == '__main__':
    check_database()
