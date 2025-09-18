from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.support import support
from app.models import db, User, ContactMessage

@support.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Us page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('All fields are required.', 'danger')
            return render_template('support/contact.html', title='Contact Us')
        
        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        
        try:
            db.session.add(contact_message)
            db.session.commit()
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('support.contact'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while sending your message. Please try again.', 'danger')
    
    return render_template('support/contact.html', title='Contact Us')

@support.route('/help')
def help():
    """Help and Documentation page"""
    return render_template('support/help.html', title='Help')

@support.route('/faq')
def faq():
    """Frequently Asked Questions page"""
    return render_template('support/faq.html', title='FAQ')
