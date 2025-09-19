#!/usr/bin/env python3
"""
Script to test registration functionality and identify issues
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User
from app.utils.password_utils import check_password_strength
from config import Config
import traceback

def debug_registration():
    """Debug the registration process"""
    print("🔍 Debugging SecureShare Registration Process")
    print("=" * 50)
    
    # Create test app
    app = create_app()
    
    with app.app_context():
        try:
            # Test 1: Database connection
            print("\n1. Testing database connection...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test 2: Password strength validation
            print("\n2. Testing password strength validation...")
            test_password = "TestPassword123!"
            strength_result = check_password_strength(test_password)
            print(f"Password: {test_password}")
            print(f"Strength result: {strength_result}")
            
            if strength_result['score'] >= 4:
                print("✅ Password meets complexity requirements")
            else:
                print(f"❌ Password fails complexity check: {strength_result['feedback']}")
            
            # Test 3: User model creation
            print("\n3. Testing User model creation...")
            test_username = "testuser"
            test_email = "test@example.com"
            
            # Check if user already exists
            existing_user = User.query.filter_by(username=test_username).first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()
                print("🗑️ Removed existing test user")
            
            # Create new user
            new_user = User(username=test_username, email=test_email)
            new_user.password = test_password
            
            print(f"User created: {new_user}")
            print(f"Password hash: {new_user.password_hash}")
            
            # Test 4: Database save operation
            print("\n4. Testing database save operation...")
            db.session.add(new_user)
            db.session.commit()
            print("✅ User saved to database successfully")
            
            # Test 5: Password verification
            print("\n5. Testing password verification...")
            if new_user.verify_password(test_password):
                print("✅ Password verification successful")
            else:
                print("❌ Password verification failed")
            
            # Test 6: User retrieval
            print("\n6. Testing user retrieval...")
            retrieved_user = User.query.filter_by(username=test_username).first()
            if retrieved_user:
                print(f"✅ User retrieved: {retrieved_user}")
                print(f"   Username: {retrieved_user.username}")
                print(f"   Email: {retrieved_user.email}")
                print(f"   Role: {retrieved_user.role}")
            else:
                print("❌ User retrieval failed")
            
            # Clean up
            print("\n7. Cleaning up...")
            db.session.delete(new_user)
            db.session.commit()
            print("✅ Test user cleaned up")
            
        except Exception as e:
            print(f"\n❌ Error occurred during testing:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"Traceback:")
            traceback.print_exc()
            
            # Try to rollback if there's an active transaction
            try:
                db.session.rollback()
                print("🔄 Database session rolled back")
            except:
                pass

def test_registration_route():
    """Test the registration route specifically"""
    print("\n🌐 Testing Registration Route")
    print("=" * 30)
    
    app = create_app()
    
    with app.test_client() as client:
        try:
            # Test 1: GET request to registration page
            print("\n1. Testing GET request to /auth/register...")
            response = client.get('/auth/register')
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                print("✅ Registration page loads successfully")
            else:
                print(f"❌ Registration page failed to load: {response.status_code}")
            
            # Test 2: POST request with valid data
            print("\n2. Testing POST request with valid data...")
            test_data = {
                'username': 'debuguser',
                'email': 'debug@example.com',
                'password': 'DebugPassword123!',
                'confirm_password': 'DebugPassword123!'
            }
            
            response = client.post('/auth/register', data=test_data, follow_redirects=True)
            print(f"Status code: {response.status_code}")
            print(f"Response data preview: {response.data[:500].decode('utf-8', errors='ignore')}")
            
            # Check if registration was successful
            with app.app_context():
                user = User.query.filter_by(username='debuguser').first()
                if user:
                    print("✅ User was created successfully in database")
                    # Clean up
                    db.session.delete(user)
                    db.session.commit()
                    print("🗑️ Test user cleaned up")
                else:
                    print("❌ User was not created in database")
            
        except Exception as e:
            print(f"\n❌ Error occurred during route testing:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            traceback.print_exc()

if __name__ == '__main__':
    debug_registration()
    test_registration_route()
    print("\n🎯 Debug Complete!")
    print("If issues were found, they should be visible in the output above.")
