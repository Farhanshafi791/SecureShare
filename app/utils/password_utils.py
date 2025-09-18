import re
from wtforms import ValidationError

def validate_password_complexity(form, field):
    """Validate password complexity requirements"""
    password = field.data
    
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter.')
    
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter.')
    
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one number.')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>).')

def check_password_strength(password):
    """Check password strength and return score and feedback"""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("One uppercase letter")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("One lowercase letter")
    
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("One number")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("One special character")
    
    strength_levels = {
        0: 'Very Weak',
        1: 'Very Weak', 
        2: 'Weak',
        3: 'Fair',
        4: 'Good',
        5: 'Strong'
    }
    
    return {
        'score': score,
        'max_score': 5,
        'strength': strength_levels.get(score, 'Unknown'),
        'feedback': feedback
    }
