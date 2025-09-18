#!/usr/bin/env python3
"""
Simple test to verify home route and template
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask import url_for

def test_home_route():
    """Test the home route and template"""
    app = create_app()
    
    with app.app_context():
        try:
            # Test URL generation
            home_url = url_for('main.home')
            print(f"✅ Home URL generated: {home_url}")
            
            # Test template exists
            template_path = os.path.join('templates', 'main', 'home.html')
            if os.path.exists(template_path):
                print("✅ home.html template exists")
            else:
                print("❌ home.html template not found")
                
            # Test client request
            with app.test_client() as client:
                response = client.get('/')
                if response.status_code == 200:
                    print("✅ Home route responds successfully (status 200)")
                    if b"SecureShare" in response.data:
                        print("✅ Home page content loads correctly")
                    else:
                        print("❌ Home page content not found")
                else:
                    print(f"❌ Home route failed with status {response.status_code}")
                    
            return True
            
        except Exception as e:
            print(f"❌ Home route test failed: {e}")
            return False

if __name__ == '__main__':
    print("Testing Home Route and Template")
    print("=" * 35)
    test_home_route()
