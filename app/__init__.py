from flask import Flask, session, request, g
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from config import Config
from datetime import datetime, timedelta

# Initialize extensions

# Import models and db
from app.models import db

# Import blueprints
from app.auth.routes import auth as auth_blueprint
from app.main.routes import main as main_blueprint
from app.admin.routes import admin as admin_blueprint
from app.support.routes import support as support_blueprint

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    from app.models import User
    db.init_app(app)
    bcrypt = Bcrypt(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.needs_refresh_message = 'Please reauthenticate to access this page.'
    login_manager.needs_refresh_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.before_request
    def check_session_timeout():
        """Check for session timeout on each request"""
        if current_user.is_authenticated:
            # Make session permanent to use PERMANENT_SESSION_LIFETIME
            session.permanent = True
            
            # Check if this is the first request (set session start time)
            if 'session_start' not in session:
                session['session_start'] = datetime.utcnow().isoformat()
                session['last_activity'] = datetime.utcnow().isoformat()
            
            # Update last activity time
            last_activity = datetime.fromisoformat(session.get('last_activity', datetime.utcnow().isoformat()))
            current_time = datetime.utcnow()
            
            # Check if session has expired
            if current_time - last_activity > app.config['PERMANENT_SESSION_LIFETIME']:
                session.clear()
                from flask_login import logout_user
                logout_user()
                from flask import flash, redirect, url_for
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Update last activity
            session['last_activity'] = current_time.isoformat()
            
            # Set warning flag if close to timeout
            time_left = app.config['PERMANENT_SESSION_LIFETIME'] - (current_time - last_activity)
            g.session_warning = time_left <= app.config['SESSION_TIMEOUT_WARNING']
            g.time_left_minutes = int(time_left.total_seconds() / 60)

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(support_blueprint, url_prefix='/support')

    return app
