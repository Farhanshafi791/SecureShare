from flask import render_template, redirect, url_for, flash, abort, Blueprint, request
from flask_login import login_required, current_user
from functools import wraps  # <--- Add this line
from app.models import db, User

admin = Blueprint('admin', __name__)

# A custom decorator to check for admin access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Admin dashboard logic goes here
    user_count = User.query.count()
    admin_count = User.query.filter_by(role='admin').count()
    regular_count = user_count - admin_count
    
    return render_template('admin/dashboard.html', 
                         user_count=user_count,
                         admin_count=admin_count,
                         regular_count=regular_count)

@admin.route('/users')
@login_required
@admin_required
def view_users():
    # View all users in the database
    try:
        users = User.query.all()
        return render_template('admin/users.html', users=users)
    except Exception as e:
        flash('Error loading users. Please try again.', 'danger')
        return redirect(url_for('admin.dashboard'))

@admin.route('/users/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    """View individual user details"""
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a specific user"""
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.view_users'))
    
    user = User.query.get_or_404(user_id)
    try:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{username}" has been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user. Please try again.', 'danger')
    
    return redirect(url_for('admin.view_users'))

# Add other admin routes like user management here