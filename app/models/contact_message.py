from datetime import datetime
from app.models import db

class ContactMessage(db.Model):
    """Model for contact form messages"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relationship
    user = db.relationship('User', backref='contact_messages')
    
    def __repr__(self):
        return f'<ContactMessage {self.subject} from {self.email}>'
