from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from . import db


class User(db.Model, UserMixin):
    """User model for authentication and user management"""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_token = db.Column(db.String(100), unique=True, nullable=True)
    
    # Profile fields
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    timezone = db.Column(db.String(50), default='UTC', nullable=True)
    language = db.Column(db.String(10), default='en', nullable=True)
    
    # Convenience property for email verification
    @property
    def email_verified(self):
        return self.is_verified
    
    # Relationships
    files = db.relationship('File', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    access_logs = db.relationship('AccessLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = 'user'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_verification_token(self):
        """Generate a verification token for email verification"""
        from flask import current_app
        import secrets
        
        # Generate a secure random token
        token = secrets.token_urlsafe(32)
        self.verification_token = token
        return token
    
    def verify_email_token(self, token):
        """Verify the email verification token"""
        if self.verification_token == token:
            self.is_verified = True
            self.verification_token = None  # Clear the token after verification
            return True
        return False
    
    @staticmethod
    def verify_token_and_get_user(token):
        """Get user by verification token"""
        return User.query.filter_by(verification_token=token).first()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"
