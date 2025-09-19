import os
from datetime import timedelta

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, which is fine for production
    pass

class Config:
    """Base configuration class with common settings."""
    
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # Handle PostgreSQL URL format for Render (postgres:// -> postgresql://)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Ensure instance directory exists for SQLite
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f'sqlite:///{os.path.join(instance_path, "site.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before use
        'pool_recycle': 300,    # Recycle connections every 5 minutes
    }
    
    # Session configuration
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT', 'false').lower() == 'true'
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600)))
    SESSION_TIMEOUT_WARNING = timedelta(seconds=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600)) - 300)
    
    # File upload configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(os.getcwd(), 'uploads')
    
    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 50 * 1024 * 1024))  # 50MB default
    
    # Parse allowed extensions from environment or use defaults
    allowed_ext_str = os.environ.get('ALLOWED_EXTENSIONS', 
        'txt,pdf,doc,docx,xls,xlsx,ppt,pptx,png,jpg,jpeg,gif,bmp,webp,svg,'
        'mp3,wav,flac,ogg,aac,m4a,wma,aiff,au,zip,rar,7z,tar,gz')
    ALLOWED_EXTENSIONS = {ext.strip() for ext in allowed_ext_str.split(',') if ext.strip()}
    
    # Security configuration
    WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', 'true').lower() in ['true', 'on', '1']
    
    # Feature flags
    ALLOW_REGISTRATION = os.environ.get('ALLOW_REGISTRATION', 'true').lower() in ['true', 'on', '1']
    REQUIRE_EMAIL_VERIFICATION = os.environ.get('REQUIRE_EMAIL_VERIFICATION', 'false').lower() in ['true', 'on', '1']
    ENABLE_ENCRYPTION = os.environ.get('ENABLE_ENCRYPTION', 'true').lower() in ['true', 'on', '1']
    
    # Encryption settings
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or 'dev-encryption-key-change-in-production'
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587)) if os.environ.get('MAIL_PORT') else None
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or os.environ.get('MAIL_USERNAME')
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    
    # Ensure instance directory exists for development
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(instance_path, "site.db")}'

class ProductionConfig(Config):
    """Production configuration for Render deployment."""
    DEBUG = False
    TESTING = False
    
    # Force secure settings in production
    WTF_CSRF_ENABLED = True
    ENABLE_ENCRYPTION = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Set up logging for production
        import logging
        from logging import StreamHandler
        
        # Create a stream handler for stdout (Render captures this)
        stream_handler = StreamHandler()
        stream_handler.setLevel(getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO))
        
        # Set up formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        stream_handler.setFormatter(formatter)
        
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO))

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    ALLOW_REGISTRATION = True
    REQUIRE_EMAIL_VERIFICATION = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}