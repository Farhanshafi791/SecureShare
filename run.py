#!/usr/bin/env python3
"""
SecureShare Application Entry Point
This is the main file to run the SecureShare application.
"""

from app import create_app
from app.models import db

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        print("✅ Database tables created/verified")
        
    print("🚀 Starting SecureShare application...")
    print("📱 Access the application at: http://localhost:5000")
    
    # Run the application
    app.run(debug=True, host='127.0.0.1', port=5000)
