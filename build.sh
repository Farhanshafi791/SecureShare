#!/usr/bin/env bash
# Render Build Script for SecureShare Flask Application

set -o errexit  # Exit on error

echo "🚀 Starting SecureShare deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p instance

echo "🗃️  Setting up database..."
python -c "
from app import create_app
from app.models import db

print('Creating application context...')
app = create_app()

with app.app_context():
    print('Creating database tables...')
    db.create_all()
    print('✅ Database tables created successfully!')
"

echo "✅ Build completed successfully!"
