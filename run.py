#!/usr/bin/env python3
"""
SecureShare Application Entry Point
This is the main file to run the SecureShare application.
"""

import os
from app import create_app
from app.models import db

# Determine the configuration environment
config_name = os.environ.get('FLASK_ENV', 'development')

# Create the Flask application with the appropriate configuration
app = create_app(config_name)

if __name__ == '__main__':
    # Only create tables and run in debug mode when running directly
    # In production (Render), this will be handled by the build script
    if config_name == 'development':
        with app.app_context():
            # Create database tables if they don't exist
            db.create_all()
            print("✅ Database tables created/verified")
            
        print("🚀 Starting SecureShare application in development mode...")
        print("📱 Access the application at: http://localhost:5000")
        
        # Run the application in development mode
        app.run(
            debug=True, 
            host=os.environ.get('HOST', '127.0.0.1'), 
            port=int(os.environ.get('PORT', 5000))
        )
    else:
        print(f"🚀 SecureShare application ready for {config_name} environment")
        # In production, gunicorn will handle running the app
        # This file serves as the WSGI entry point
