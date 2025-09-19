from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin
from app.models import db, User
from app.utils.password_utils import check_password_strength
import re

auth = Blueprint('auth', __name__)

def is_safe_url(target):
    """Check if the target URL is safe for redirects"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_redirect_target():
    """Get the next URL from request args or referrer"""
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
    return None

def redirect_back(endpoint, **values):
    """Redirect back to the previous page or to a default endpoint"""
    target = get_redirect_target()
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already authenticated, redirect to appropriate dashboard
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')
        
        # Validate password complexity
        password_check = check_password_strength(password)
        if password_check['score'] < 4:  # Require at least "Good" strength
            flash('Password does not meet complexity requirements: ' + ', '.join(password_check['feedback']), 'danger')
            return render_template('auth/register.html')
        
        # Check if username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'danger')
            return render_template('auth/register.html')
        
        # Check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'danger')
            return render_template('auth/register.html')

        try:
            new_user = User(username=username, email=email)
            new_user.password = password  # This will trigger the password setter
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already authenticated, redirect to appropriate dashboard
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email_or_username = request.form.get('email') or request.form.get('username')
        password = request.form.get('password')
        
        # Validate input
        if not email_or_username or not password:
            flash('Email/Username and password are required.', 'danger')
            return render_template('auth/login.html')
        
        # Try to find user by email first, then by username
        user = User.query.filter_by(email=email_or_username).first()
        if not user:
            user = User.query.filter_by(username=email_or_username).first()
            
        if user and user.verify_password(password):
            login_user(user, remember=True)
            
            # Get next page parameter
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            
            # Redirect based on user role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email/username or password.', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    flash('You have been logged out successfully.', 'info')
    logout_user()
    # Redirect to home page instead of login to avoid confusion
    return redirect(url_for('main.home'))