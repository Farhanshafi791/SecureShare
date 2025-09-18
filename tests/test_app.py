#!/usr/bin/env python3
"""
Test script to verify the Flask app can start successfully
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_app_startup():
    """Test if the Flask app can be created and configured properly"""
    try:
        app = create_app()
        print("✅ Flask app created successfully!")
        
        # Test app configuration
        print(f"✅ Debug mode: {app.debug}")
        print(f"✅ Database URI configured: {bool(app.config.get('SQLALCHEMY_DATABASE_URI'))}")
        
        # Test routes
        with app.app_context():
            print("✅ App context created successfully!")
            
            # List available routes
            print("\nAvailable routes:")
            for rule in app.url_map.iter_rules():
                methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
                print(f"  {rule.endpoint:20} {methods:10} {rule}")
        
        print("\n🎉 Flask application is ready to run!")
        print("You can start it with: python app.py")
        
        return True
    except Exception as e:
        print(f"❌ App startup test failed: {e}")
        return False

if __name__ == '__main__':
    print("SecureShare Flask App Startup Test")
    print("=" * 40)
    test_app_startup()
