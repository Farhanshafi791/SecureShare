import os
from flask import render_template, Blueprint, redirect, url_for, request, flash, send_file, current_app, abort, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime

from app.models import db, File, AccessLog, User
from app.main.forms import ProfileForm, ChangePasswordForm
from app.utils.file_utils import (
    allowed_file, generate_unique_filename, get_file_path, 
    ensure_upload_directory, encrypt_file, decrypt_file, 
    get_mime_type, delete_file, is_audio_file, is_image_file,
    is_document_file, get_file_category, get_file_icon_class
)

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # If user is already logged in, offer to go to dashboard
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))
    return render_template('main/home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Redirect admin users to admin dashboard
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    
    # Get user's recent files
    recent_files = current_user.files.order_by(File.upload_time.desc()).limit(5).all()
    total_files = current_user.files.count()
    
    # Calculate total downloads from access logs
    total_downloads = db.session.query(AccessLog).filter_by(
        user_id=current_user.id, action='download'
    ).count()
    
    # Calculate active shares (files that have been shared)
    active_shares = db.session.query(AccessLog).filter_by(
        user_id=current_user.id, action='share'
    ).distinct(AccessLog.file_id).count()
    
    # Calculate total storage used
    total_size = sum(file.file_size or 0 for file in current_user.files)
    total_size_mb = total_size / (1024 * 1024)
    
    # Storage limit (in MB) - this could be configurable per user
    storage_limit_mb = 100  # Default 100MB limit
    
    # Create recent activity data
    recent_activity = []
    recent_logs = AccessLog.query.filter_by(user_id=current_user.id)\
        .order_by(AccessLog.timestamp.desc()).limit(5).all()
    
    for log in recent_logs:
        activity = {
            'description': f'You {log.action}ed a file',
            'timestamp': log.timestamp,
            'icon': 'fa-upload' if log.action == 'upload' else 'fa-download' if log.action == 'download' else 'fa-share',
            'color': 'success' if log.action == 'upload' else 'primary' if log.action == 'download' else 'info'
        }
        if log.file:
            activity['description'] = f'You {log.action}ed "{log.file.original_filename}"'
        recent_activity.append(activity)
    
    # Calculate file type statistics
    audio_files = 0
    image_files = 0
    document_files = 0
    other_files = 0
    
    for file in current_user.files:
        category = get_file_category(file.original_filename)
        if category == 'audio':
            audio_files += 1
        elif category == 'image':
            image_files += 1
        elif category == 'document':
            document_files += 1
        else:
            other_files += 1
    
    return render_template('main/dashboard.html', 
                         user=current_user, 
                         recent_files=recent_files,
                         total_files=total_files,
                         total_downloads=total_downloads,
                         active_shares=active_shares,
                         total_size_mb=total_size_mb,
                         storage_limit_mb=storage_limit_mb,
                         recent_activity=recent_activity,
                         audio_files=audio_files,
                         image_files=image_files,
                         document_files=document_files,
                         other_files=other_files,
                         get_file_icon_class=get_file_icon_class,
                         get_file_category=get_file_category)

@main.route('/files')
@login_required
def files():
    """View all user files"""
    page = request.args.get('page', 1, type=int)
    files = current_user.files.order_by(File.upload_time.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('main/files.html', 
                         files=files,
                         get_file_icon_class=get_file_icon_class,
                         get_file_category=get_file_category)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        print("Upload POST request received")  # Debug
        
        # Check if file was uploaded
        if 'file' not in request.files:
            print("No file in request.files")  # Debug
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        print(f"File received: {file.filename}")  # Debug
        
        # Check if file was actually selected
        if file.filename == '':
            print("Empty filename")  # Debug
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        # Validate file
        if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            print("File validation passed")  # Debug
            try:
                # Ensure upload directory exists
                ensure_upload_directory(current_app.config['UPLOAD_FOLDER'])
                print("Upload directory ensured")  # Debug
                
                # Generate unique filename
                unique_filename = generate_unique_filename(file.filename)
                file_path = get_file_path(current_app.config['UPLOAD_FOLDER'], unique_filename)
                print(f"File path: {file_path}")  # Debug
                
                # Read and encrypt file data
                file_data = file.read()
                print(f"File data read: {len(file_data)} bytes")  # Debug
                encrypted_data = encrypt_file(file_data)
                print("File encrypted")  # Debug
                
                # Save encrypted file
                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)
                print("Encrypted file saved")  # Debug
                
                # Create file record in database
                new_file = File(
                    filename=unique_filename,
                    original_filename=secure_filename(file.filename),
                    encrypted_path=file_path,
                    file_size=len(file_data),
                    mime_type=get_mime_type(file.filename),
                    owner_id=current_user.id
                )
                print("File object created")  # Debug
                
                db.session.add(new_file)
                db.session.flush()  # This assigns the ID without committing
                print(f"File added to session with ID: {new_file.id}")  # Debug
                
                # Log the upload action
                log_entry = AccessLog(
                    action='upload',
                    user_id=current_user.id,
                    file_id=new_file.id
                )
                db.session.add(log_entry)
                print("Access log created")  # Debug
                
                db.session.commit()
                print("Database committed")  # Debug
                
                flash(f'File "{file.filename}" uploaded successfully!', 'success')
                return redirect(url_for('main.files'))
                
            except Exception as e:
                print(f"Upload error: {e}")  # Debug
                import traceback
                traceback.print_exc()
                db.session.rollback()
                flash(f'Error uploading file: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            print(f"File validation failed for: {file.filename}")  # Debug
            flash('File type not allowed. Please upload a valid file.', 'danger')
            return redirect(request.url)
    
    return render_template('main/upload.html')

@main.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """Download a file (owner only)"""
    file_record = File.query.get_or_404(file_id)
    
    # Check if user owns the file
    if file_record.owner_id != current_user.id:
        abort(403)  # Forbidden
    
    try:
        # Read encrypted file
        with open(file_record.encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt file data
        decrypted_data = decrypt_file(encrypted_data)
        
        # Create temporary file for download
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(decrypted_data)
        temp_file.close()
        
        # Update download count
        file_record.download_count += 1
        
        # Log the download action
        log_entry = AccessLog(
            action='download',
            user_id=current_user.id,
            file_id=file_record.id
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=file_record.original_filename,
            mimetype=file_record.mime_type
        )
        
    except Exception as e:
        flash('Error downloading file. Please try again.', 'danger')
        return redirect(url_for('main.files'))


@main.route('/shared/<token>')
def download_shared_file(token):
    """Download a file using a share token (no login required)"""
    print(f"🔍 Attempting to download file with token: {token}")
    
    try:
        file_record = File.query.filter_by(share_token=token, is_shared=True).first()
        print(f"🔍 Database query result: {file_record}")
        
        if not file_record:
            print("❌ No file found with this token")
            flash('File not found or link is invalid.', 'danger')
            return redirect(url_for('main.home'))
        
        print(f"📁 Found file: {file_record.original_filename}")
        print(f"🔍 Encrypted file path: {file_record.encrypted_path}")
        
        # Read the encrypted file content
        with open(file_record.encrypted_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        print(f"📊 Encrypted data size: {len(encrypted_data)} bytes")
        
        # Decrypt the file
        decrypted_content = decrypt_file(encrypted_data)
        print(f"🔓 File decrypted successfully, size: {len(decrypted_content)} bytes")
        
        # Create temporary file for download
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_' + file_record.filename)
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(decrypted_content)
        
        print(f"💾 Temporary file created at: {temp_path}")
        
        # Update download count
        file_record.download_count += 1
        db.session.commit()
        
        # Log the download action (anonymous user)
        log_entry = AccessLog(
            action='download',
            user_id=None,  # Anonymous download
            file_id=file_record.id
        )
        db.session.add(log_entry)
        db.session.commit()
        
        print("📊 Download logged successfully")
        
        # Send the file
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=file_record.original_filename,
            mimetype=file_record.mime_type
        )
        
    except Exception as e:
        print(f"❌ Error in download_shared_file: {e}")
        import traceback
        traceback.print_exc()
        flash('Error downloading file. The share link may be invalid or expired.', 'danger')
        return redirect(url_for('main.home'))

@main.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_user_file(file_id):
    """Delete a file"""
    file_record = File.query.get_or_404(file_id)
    
    # Check if user owns the file
    if file_record.owner_id != current_user.id:
        abort(403)  # Forbidden
    
    try:
        # Delete physical file
        delete_file(file_record.encrypted_path)
        
        # Log the delete action
        log_entry = AccessLog(
            action='delete',
            user_id=current_user.id,
            file_id=file_record.id
        )
        db.session.add(log_entry)
        
        # Delete database record
        db.session.delete(file_record)
        db.session.commit()
        
        flash('File deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Error deleting file. Please try again.', 'danger')
    
    return redirect(url_for('main.files'))

@main.route('/share/<int:file_id>', methods=['POST'])
@login_required
def toggle_share_file(file_id):
    """Generate or revoke file sharing link"""
    file_record = File.query.get_or_404(file_id)
    
    # Check if user owns the file
    if file_record.owner_id != current_user.id:
        abort(403)  # Forbidden
    
    try:
        if file_record.is_shared:
            # Revoke sharing
            file_record.revoke_share_token()
            flash('File sharing disabled. The link is no longer valid.', 'info')
        else:
            # Generate share token
            file_record.generate_share_token()
            flash('File sharing enabled! Share link copied to clipboard.', 'success')
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        flash('Error updating file sharing status. Please try again.', 'danger')
    
    return redirect(url_for('main.files'))


@main.route('/view/<int:file_id>')
@login_required
def view_file(file_id):
    """View file details"""
    file_record = File.query.get_or_404(file_id)
    
    # Check if user owns the file
    if file_record.owner_id != current_user.id:
        abort(403)
    
    # Get file category and stats
    category = get_file_category(file_record.original_filename)
    icon_class = get_file_icon_class(file_record.original_filename)
    
    # Get download history for this file
    download_logs = AccessLog.query.filter_by(
        file_id=file_record.id, action='download'
    ).order_by(AccessLog.timestamp.desc()).limit(10).all()
    
    return render_template('main/view_file.html', 
                         file=file_record,
                         category=category,
                         icon_class=icon_class,
                         download_logs=download_logs)


@main.route('/get_share_link/<int:file_id>')
@login_required
def get_share_link(file_id):
    """Get the share link for a file (AJAX endpoint)"""
    file_record = File.query.get_or_404(file_id)
    
    # Check if user owns the file
    if file_record.owner_id != current_user.id:
        abort(403)
    
    if file_record.is_shared and file_record.share_token:
        share_url = url_for('main.download_shared_file', token=file_record.share_token, _external=True)
        return jsonify({'share_url': share_url})
    else:
        return jsonify({'error': 'File is not shared'}), 400


@main.route('/profile')
@login_required
def profile():
    """View and edit user profile"""
    form = ProfileForm(obj=current_user)
    password_form = ChangePasswordForm()
    
    # Calculate user stats
    stats = {
        'total_files': current_user.files.count(),
        'total_downloads': db.session.query(AccessLog).filter_by(
            user_id=current_user.id, action='download'
        ).count(),
        'storage_used_mb': sum(file.file_size or 0 for file in current_user.files) / (1024 * 1024)
    }
    
    return render_template('main/profile.html', 
                         form=form, 
                         password_form=password_form,
                         stats=stats)


@main.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        try:
            # Check if username is taken by another user
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Username already taken. Please choose a different one.', 'danger')
                return redirect(url_for('main.profile'))
            
            # Check if email is taken by another user
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email and existing_email.id != current_user.id:
                flash('Email already registered. Please choose a different one.', 'danger')
                return redirect(url_for('main.profile'))
            
            # Update user information
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.bio = form.bio.data
            current_user.timezone = form.timezone.data
            current_user.language = form.language.data
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('main.profile'))


@main.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        try:
            # Verify current password
            if not current_user.verify_password(form.current_password.data):
                flash('Current password is incorrect.', 'danger')
                return redirect(url_for('main.profile'))
            
            # Update password
            current_user.password = form.new_password.data
            
            db.session.commit()
            flash('Password changed successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Error changing password. Please try again.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('main.profile'))