#!/usr/bin/env bash
# Render Build Script for SecureShare

set -o errexit  # Exit on any error

echo "🚀 Starting SecureShare build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p instance
mkdir -p logs

# Set proper permissions for directories
echo "🔐 Setting directory permissions..."
chmod 755 uploads
chmod 755 instance  
chmod 755 logs

# Initialize database tables
echo "🗄️ Initializing database..."
python << EOF
import os
import sys

# Set Flask environment if not already set
if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'production'

# Add the project root to Python path
sys.path.insert(0, os.getcwd())

try:
    from app import create_app
    from app.models import db
    
    print("Creating Flask application...")
    app = create_app('production')
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if admin user should be created
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        if admin_email and admin_password:
            from app.models import User
            
            # Check if admin already exists
            existing_admin = User.query.filter_by(email=admin_email).first()
            if not existing_admin:
                admin_user = User(
                    username='admin',
                    email=admin_email,
                    role='admin',
                    is_verified=True
                )
                admin_user.password = admin_password
                
                db.session.add(admin_user)
                db.session.commit()
                print(f"✅ Admin user created: {admin_email}")
            else:
                print(f"ℹ️ Admin user already exists: {admin_email}")
        else:
            print("ℹ️ No admin credentials provided (ADMIN_EMAIL/ADMIN_PASSWORD)")
            
except Exception as e:
    print(f"❌ Error during database initialization: {e}")
    sys.exit(1)
EOF

# Clean up cache files
echo "🧹 Cleaning up cache files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "✅ Build completed successfully!"
echo "🚀 Ready for deployment!"
