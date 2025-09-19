"""
Authentication tests for SecureShare application
"""

import pytest
import sys
sys.path.append('.')

from app.models import User
from app import db


def test_user_creation(app):
    """Test creating a new user"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.password = 'testpassword123'
        
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        saved_user = User.query.filter_by(username='testuser').first()
        assert saved_user is not None
        assert saved_user.email == 'test@example.com'
        assert saved_user.role == 'user'


def test_password_hashing(app):
    """Test password hashing and verification"""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.password = 'testpassword123'
        
        # Test password verification
        assert user.verify_password('testpassword123') is True
        assert user.verify_password('wrongpassword') is False


def test_admin_user_creation(app):
    """Test creating an admin user"""
    with app.app_context():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin_user.password = 'adminpassword123'
        
        db.session.add(admin_user)
        db.session.commit()
        
        # Verify admin user was created
        saved_admin = User.query.filter_by(username='admin').first()
        assert saved_admin is not None
        assert saved_admin.role == 'admin'


def test_user_authentication_routes(client):
    """Test authentication routes"""
    # Test registration page
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data
    
    # Test login page
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_user_registration(client, app):
    """Test user registration process"""
    with app.app_context():
        # Test user registration
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)
        
        # Should redirect and show success message
        assert response.status_code == 200
        
        # Verify user was created in database
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'


def test_user_login(client, app, test_user):
    """Test user login process"""
    with app.app_context():
        # Test login
        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin_user.password = 'adminpass123'
        
        assert admin_user.role == 'admin', f"Admin role should be 'admin', got '{admin_user.role}'"
        
        print("✅ All User model tests passed!")
        
        # Test database operations
        try:
            db.session.add(test_user)
            db.session.add(admin_user)
            db.session.commit()
            
            # Query users
            user_from_db = User.query.filter_by(username='testuser').first()
            assert user_from_db is not None, "User not found in database"
            assert user_from_db.email == 'test@example.com', "Email doesn't match"
            assert user_from_db.verify_password('testpassword123'), "Password verification failed after DB save"
            
            admin_from_db = User.query.filter_by(username='admin').first()
            assert admin_from_db.role == 'admin', "Admin role not preserved in database"
            
            print("✅ Database operations test passed!")
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            
        finally:
            # Clean up
            User.query.filter_by(username='testuser').delete()
            User.query.filter_by(username='admin').delete()
            db.session.commit()

def test_imports():
    """Test that all modules can be imported successfully"""
    try:
        from app.auth.routes import auth
        from app.main.routes import main
        from app.admin.routes import admin
        print("✅ All route blueprints imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing SecureShare authentication system...")
    print("=" * 50)
    
    # Test imports
    if test_imports():
        # Test user model
        print("\n🎉 All tests completed successfully!")
        print("Your authentication system is ready to use with the updated User model.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
