"""Tests for the User model"""
import pytest
from app.models import User, db


def test_user_creation(app):
    """Test user creation with default values"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.password = 'testpass123'
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'user'  # Default role
        assert user.verify_password('testpass123')
        assert not user.verify_password('wrongpass')


def test_admin_user_creation(app):
    """Test admin user creation"""
    with app.app_context():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.password = 'adminpass123'
        
        assert admin.role == 'admin'
        assert admin.verify_password('adminpass123')


def test_password_hashing(app):
    """Test password hashing functionality"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.password = 'mypassword'
        
        # Password should be hashed
        assert user.password_hash is not None
        assert user.password_hash != 'mypassword'
        
        # Should be able to verify correct password
        assert user.verify_password('mypassword')
        assert not user.verify_password('wrongpassword')


def test_user_repr(app):
    """Test user string representation"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        expected = "User('testuser', 'test@example.com', 'user')"
        assert repr(user) == expected
