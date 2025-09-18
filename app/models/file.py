from datetime import datetime
import secrets
from . import db


class File(db.Model):
    """File model for secure file storage and sharing"""
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    encrypted_path = db.Column(db.String(300), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    mime_type = db.Column(db.String(100), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_shared = db.Column(db.Boolean, default=False)
    share_token = db.Column(db.String(64), unique=True, nullable=True)  # Secure token for sharing
    download_count = db.Column(db.Integer, default=0)
    
    # Relationship to access logs
    access_logs = db.relationship('AccessLog', backref='file', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"File('{self.original_filename}', Owner ID: {self.owner_id})"
    
    @property
    def formatted_size(self):
        """Return human-readable file size"""
        size = self.file_size
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def generate_share_token(self):
        """Generate a secure token for file sharing"""
        self.share_token = secrets.token_urlsafe(32)
        self.is_shared = True
        return self.share_token
    
    def revoke_share_token(self):
        """Revoke the share token and disable sharing"""
        self.share_token = None
        self.is_shared = False
