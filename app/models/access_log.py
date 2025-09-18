from datetime import datetime
from . import db


class AccessLog(db.Model):
    """Access log model for tracking user actions on files"""
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)  # 'upload', 'download', 'delete'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Can be NULL for anonymous downloads
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)

    def __repr__(self):
        return f"AccessLog(Action: {self.action}, User ID: {self.user_id}, File ID: {self.file_id})"
