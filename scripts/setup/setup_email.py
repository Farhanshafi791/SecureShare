#!/usr/bin/env python3
"""
Quick setup script for email configuration
"""

import os
import sys

def setup_email_config():
    """Interactive setup for email configuration"""
    
    print("🔧 SecureShare Email Configuration Setup")
    print("=" * 50)
    print()
    
    print("📧 Gmail Setup Instructions:")
    print("1. Enable 2-Factor Authentication on your Gmail account")
    print("2. Generate an App Password (not your regular password)")
    print("3. Enter the details below")
    print()
    
    # Get user input
    gmail_address = input("Enter your Gmail address: ").strip()
    app_password = input("Enter your Gmail App Password (16 characters): ").strip().replace(" ", "")
    
    # Validate input
    if not gmail_address or "@gmail.com" not in gmail_address:
        print("❌ Please enter a valid Gmail address")
        return False
    
    if len(app_password) != 16:
        print("❌ App Password should be 16 characters long")
        return False
    
    # Create .env file
    env_content = f"""# SecureShare Email Configuration
MAIL_USERNAME={gmail_address}
MAIL_PASSWORD={app_password}
MAIL_DEFAULT_SENDER={gmail_address}

# Optional: Customize these if needed
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ Email configuration saved to .env file")
        print("📝 Remember to restart the application for changes to take effect")
        print()
        print("🔒 Security Notes:")
        print("   - Your .env file is automatically ignored by Git")
        print("   - Never share your App Password with anyone")
        print("   - You can regenerate App Passwords anytime in Google Account settings")
        print()
        print("🚀 To test the configuration, run:")
        print("   python scripts/test_email.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False

def load_env_file():
    """Load environment variables from .env file"""
    try:
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
            print("✅ Loaded .env file")
            return True
    except Exception as e:
        print(f"❌ Error loading .env file: {e}")
    return False

def check_current_config():
    """Check current email configuration"""
    print("\n🔍 Current Email Configuration:")
    print("-" * 30)
    
    # Load .env if exists
    load_env_file()
    
    mail_user = os.environ.get('MAIL_USERNAME')
    mail_pass = os.environ.get('MAIL_PASSWORD')
    mail_sender = os.environ.get('MAIL_DEFAULT_SENDER')
    
    print(f"MAIL_USERNAME: {'✅ SET' if mail_user else '❌ NOT SET'}")
    print(f"MAIL_PASSWORD: {'✅ SET' if mail_pass else '❌ NOT SET'}")
    print(f"MAIL_DEFAULT_SENDER: {'✅ SET' if mail_sender else '❌ NOT SET'}")
    
    if mail_user and mail_pass:
        print("\n✅ Email appears to be configured correctly!")
        return True
    else:
        print("\n❌ Email configuration incomplete")
        return False

def main():
    """Main setup function"""
    
    print("Select an option:")
    print("1. Setup new email configuration")
    print("2. Check current configuration")
    print("3. View setup instructions")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        setup_email_config()
    elif choice == "2":
        check_current_config()
    elif choice == "3":
        print("\n📖 Setup Instructions:")
        print("1. Go to your Google Account (myaccount.google.com)")
        print("2. Click 'Security' → '2-Step Verification' → Enable it")
        print("3. Go to 'App passwords' → Generate password for 'Mail'")
        print("4. Run this script again and choose option 1")
        print("5. Enter your Gmail and the 16-character app password")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
