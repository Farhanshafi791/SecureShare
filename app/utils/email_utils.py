"""
Email utilities for sending verification emails
"""

from flask import current_app, render_template, url_for
from flask_mail import Message
import threading


def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            from app import mail
            mail.send(msg)
            print(f"✅ Email sent successfully to {msg.recipients[0]}")
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            current_app.logger.error(f"Failed to send email: {str(e)}")


def send_email(to, subject, template, **kwargs):
    """Send email with template"""
    try:
        app = current_app._get_current_object()
        
        # Check if email is configured
        if not app.config.get('MAIL_USERNAME'):
            print("⚠️  Email not configured - MAIL_USERNAME not set")
            return False
        
        msg = Message(
            subject=app.config.get('MAIL_SUBJECT_PREFIX', '') + subject,
            recipients=[to],
            sender=app.config.get('MAIL_DEFAULT_SENDER') or app.config.get('MAIL_USERNAME')
        )
        
        try:
            msg.body = render_template(template + '.txt', **kwargs)
            msg.html = render_template(template + '.html', **kwargs)
        except Exception as e:
            print(f"❌ Failed to render email template: {str(e)}")
            return False
        
        # Send email in a background thread
        print(f"📧 Sending email to {to}...")
        thr = threading.Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return True
        
    except Exception as e:
        print(f"❌ Error preparing email: {str(e)}")
        current_app.logger.error(f"Error preparing email: {str(e)}")
        return False


def send_verification_email(user):
    """Send email verification email to user"""
    try:
        print(f"🔄 Generating verification token for {user.email}...")
        token = user.generate_verification_token()
        verification_url = url_for('auth.verify_email', token=token, _external=True)
        
        print(f"🔗 Verification URL: {verification_url}")
        
        result = send_email(
            to=user.email,
            subject='Please verify your email address',
            template='email/verify_email',
            user=user,
            verification_url=verification_url
        )
        
        if result:
            print(f"✅ Verification email queued for {user.email}")
            return True
        else:
            print(f"❌ Failed to queue verification email for {user.email}")
            return False
            
    except Exception as e:
        print(f"❌ Error in send_verification_email: {str(e)}")
        current_app.logger.error(f"Failed to send verification email: {str(e)}")
        return False


def send_welcome_email(user):
    """Send welcome email after successful verification"""
    try:
        result = send_email(
            to=user.email,
            subject='Welcome to SecureShare!',
            template='email/welcome',
            user=user
        )
        
        if result:
            print(f"✅ Welcome email queued for {user.email}")
            return True
        else:
            print(f"❌ Failed to queue welcome email for {user.email}")
            return False
            
    except Exception as e:
        print(f"❌ Error in send_welcome_email: {str(e)}")
        current_app.logger.error(f"Failed to send welcome email: {str(e)}")
        return False
