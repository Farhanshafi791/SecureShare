#!/usr/bin/env python3
import sys
import traceback
from sqlalchemy.exc import IntegrityError

sys.path.append('.')

from app import create_app
from app.models import db, ContactMessage

def run_support_system_tests():
    print("Testing Support System")
    print("=" * 30)

    app = create_app()
    client = app.test_client()

    with app.app_context():
        db.create_all()
        ContactMessage.query.filter(ContactMessage.email.like('%test@example.com')).delete()
        db.session.commit()

        try:
            print("\nTesting direct contact message creation...")
            message = ContactMessage(
                name='Test User DB',
                email='db-test@example.com',
                subject='Test Subject DB',
                message='This is a test message for the database.'
            )
            db.session.add(message)
            db.session.commit()

            saved_message = ContactMessage.query.filter_by(email='db-test@example.com').first()
            assert saved_message is not None, "Message was not saved to the database"
            assert saved_message.name == 'Test User DB'
            assert saved_message.subject == 'Test Subject DB'
            print("✅ Contact message created and verified in the database")

            db.session.delete(saved_message)
            db.session.commit()

            print("\nTesting support system web routes...")
            
            response_contact = client.get('/support/contact')
            assert response_contact.status_code == 200, f"Expected status 200, got {response_contact.status_code}"
            assert b'Contact Us' in response_contact.data, "Contact page content is missing"
            print(f"✅ Contact page loaded successfully (Status {response_contact.status_code})")

            response_help = client.get('/support/help')
            assert response_help.status_code == 200, f"Expected status 200, got {response_help.status_code}"
            assert b'Help Center' in response_help.data, "Help page content is missing"
            print(f"✅ Help page loaded successfully (Status {response_help.status_code})")
            
            print("\nTesting contact form submission...")
            response_post = client.post('/support/contact', data={
                'name': 'Test Form User',
                'email': 'form-test@example.com',
                'subject': 'Form Subject',
                'message': 'This is a test message from the form.'
            }, follow_redirects=True)

            assert response_post.status_code == 200, "Form submission failed"
            print(f"✅ Contact form submitted successfully (Status {response_post.status_code})")

            form_message = ContactMessage.query.filter_by(email='form-test@example.com').first()
            assert form_message is not None, "Form submission data not found in database"
            assert form_message.name == 'Test Form User'
            print("✅ Form data correctly saved to the database")

            print("\nTesting contact message validation (e.g., NULL name)...")
            validation_failed = False
            try:
                invalid_message = ContactMessage(
                    name=None,
                    email='invalid@example.com',
                    subject='Invalid',
                    message='This message should not be saved.'
                )
                db.session.add(invalid_message)
                db.session.commit()
            except IntegrityError:
                validation_failed = True
                db.session.rollback()
            
            assert validation_failed, "Validation failed: A message with a NULL name was committed."
            print("✅ Database correctly rejected invalid message due to NOT NULL constraint")

            print("\n🎉 All support system tests passed!")

        finally:
            ContactMessage.query.filter(ContactMessage.email.like('%test@example.com')).delete()
            db.session.commit()
            print("🧹 Test cleanup completed")

if __name__ == '__main__':
    print("SecureShare Support System Tests")
    print("=" * 40)
    
    try:
        run_support_system_tests()
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)