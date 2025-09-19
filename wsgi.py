#!/usr/bin/env python3
"""
Production startup script for SecureShare Flask application.
This script is optimized for deployment on cloud platforms like Render.
"""

import os
from app import create_app
from app.models import db

# Create Flask application
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Run the application
    app.run(host=host, port=port, debug=False)
