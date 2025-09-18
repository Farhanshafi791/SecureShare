#!/usr/bin/env python3
"""
Email debugging script to test email configuration
"""

import sys
import os

# Add the parent directory to the path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, User
from app.utils.email_utils import send_verification_email

def test_email_configuration():
    """Test email configuration and functionality"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Testing Email Configuration")
        print("=" * 50)
        
        # Check configuration
        print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
        print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
        print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
        print(f"MAIL_USERNAME: {'***SET***' if app.config.get('MAIL_USERNAME') else 'NOT SET'}")
        print(f"MAIL_PASSWORD: {'***SET***' if app.config.get('MAIL_PASSWORD') else 'NOT SET'}")
        print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
        
        print("\n📧 Testing Email Functionality")
        print("-" * 30)
        
        # Create a test user
        test_user = User(
            username='testuser',
            email='test@example.com'
        )
        test_user.password = 'testpassword'
        
        try:
            # Test email sending (won't actually send due to fake email)
            result = send_verification_email(test_user)
            
            if result:
                print("✅ Email function executed successfully")
            else:
                print("❌ Email function failed")
                
        except Exception as e:
            print(f"❌ Error testing email: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_email_configuration()
