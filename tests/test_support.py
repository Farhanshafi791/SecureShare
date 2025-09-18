"""
Support system tests for SecureShare application
"""

import pytest
from app.models import ContactMessage
from app import db


def test_contact_message_creation(app):
    """Test creating a contact message"""
    with app.app_context():
        message = ContactMessage(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='This is a test message'
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Verify message was created
        saved_message = ContactMessage.query.filter_by(email='test@example.com').first()
        assert saved_message is not None
        assert saved_message.name == 'Test User'
        assert saved_message.subject == 'Test Subject'
        assert saved_message.message == 'This is a test message'


def test_support_routes(client):
    """Test support system routes"""
    # Test contact page
    response = client.get('/support/contact')
    assert response.status_code == 200
    assert b'Contact' in response.data
    
    # Test help page
    response = client.get('/support/help')
    assert response.status_code == 200
    assert b'Help' in response.data


def test_contact_form_submission(client, app):
    """Test contact form submission"""
    with app.app_context():
        response = client.post('/support/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify message was saved to database
        message = ContactMessage.query.filter_by(email='test@example.com').first()
        assert message is not None
        assert message.name == 'Test User'


def test_contact_message_validation(app):
    """Test contact message validation"""
    with app.app_context():
        # Test with missing required fields
        message = ContactMessage(
            name='',  # Empty name should fail validation
            email='test@example.com',
            subject='Test Subject',
            message='This is a test message'
        )
        
        # Should raise validation error when trying to commit
        with pytest.raises(Exception):
            db.session.add(message)
            db.session.commit()
