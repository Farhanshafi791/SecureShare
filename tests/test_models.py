#!/usr/bin/env python3
"""
Tests for the User model
"""

import sys
import traceback

# Add the project root to the Python path
sys.path.append('.')

# Imports from the application
from app import create_app
from app.models import db, User

def run_user_model_tests():
    """Execute all tests for the User model"""
    print("Testing User Model")
    print("=" * 30)
    
    # Create a Flask app instance
    app = create_app()
    
    # Work within the application and database context
    with app.app_context():
        # Ensure the database tables are created
        db.create_all()
        
        # Clean up any existing test data to ensure a clean slate
        User.query.filter(User.username.like('test%')).delete()
        User.query.filter_by(username='admin').delete()
        db.session.commit()
        
        try:
            # --- Test 1: Standard User Creation ---
            print("\nTesting user creation with default values...")
            user = User(username='testuser', email='test@example.com')
            user.password = 'testpass123'
            
            db.session.add(user)
            db.session.commit()
            
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.role == 'user', f"Default role should be 'user', but got '{user.role}'"
            print("✅ User properties and default role are correct")
            
            assert user.verify_password('testpass123'), "Password verification failed for correct password"
            assert not user.verify_password('wrongpass'), "Password verification succeeded for incorrect password"
            print("✅ Password verification works correctly")

            # --- Test 2: Admin User Creation ---
            print("\nTesting admin user creation...")
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.password = 'adminpass123'
            
            db.session.add(admin)
            db.session.commit()

            assert admin.role == 'admin', "Admin role was not set correctly"
            assert admin.verify_password('adminpass123'), "Admin password verification failed"
            print("✅ Admin user created successfully")

            # --- Test 3: Password Hashing ---
            print("\nTesting password hashing functionality...")
            hash_user = User(username='testuser2', email='test2@example.com')
            hash_user.password = 'mypassword'

            assert hash_user.password_hash is not None, "Password hash should not be None"
            assert hash_user.password_hash != 'mypassword', "Password should be hashed, not stored in plaintext"
            print("✅ Password hash is generated and not plaintext")
            
            assert hash_user.verify_password('mypassword'), "Hashed password could not be verified"
            assert not hash_user.verify_password('wrongpassword'), "Verification succeeded for wrong password"
            print("✅ Hashed password verification is correct")

            # --- Test 4: User String Representation ---
            print("\nTesting user string representation (__repr__)...")
            repr_user = User(username='testrepr', email='repr@example.com')
            expected_repr = "User('testrepr', 'repr@example.com', 'user')"
            assert repr(repr_user) == expected_repr, f"Repr was '{repr(repr_user)}', expected '{expected_repr}'"
            print(f"✅ User representation is correct: {repr(repr_user)}")

            print("\n🎉 All user model tests passed!")

        finally:
            # --- Cleanup ---
            # Rollback any failed transactions and clean the database
            db.session.rollback()
            User.query.filter(User.username.like('test%')).delete()
            User.query.filter_by(username='admin').delete()
            db.session.commit()
            print("🧹 Test cleanup completed")


if __name__ == '__main__':
    print("SecureShare User Model Tests")
    print("=" * 40)
    
    try:
        run_user_model_tests()
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)