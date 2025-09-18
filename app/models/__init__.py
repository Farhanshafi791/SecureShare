from flask_sqlalchemy import SQLAlchemy

# Initialize database
db = SQLAlchemy()

# Import all models to make them available when importing from app.models
from .user import User
from .file import File
from .access_log import AccessLog
from .contact_message import ContactMessage

__all__ = ['db', 'User', 'File', 'AccessLog', 'ContactMessage']
