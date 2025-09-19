#!/usr/bin/env python3
"""
Test script for file upload and download functionality
"""

import sys
import os
import tempfile
import io

sys.path.append('.')

from app import create_app
from app.models import db, User, File, AccessLog

def test_file_operations():
    """Test file upload, download, and delete operations"""
    print("Testing File Operations")
    print("=" * 30)
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Clean up any existing test data
        User.query.filter_by(username='testfileuser').delete()
        db.session.commit()
        
        # Create a test user
        test_user = User(
            username='testfileuser',
            email='testfile@example.com'
        )
        test_user.password = 'testpassword123'
        
        db.session.add(test_user)
        db.session.commit()
        
        print(f"✅ Created test user: {test_user.username}")
        
        # Test file creation
        test_file_content = b"This is a test file content for SecureShare testing."
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            temp_file.write(test_file_content)
            temp_file_path = temp_file.name
        
        try:
            # Test file encryption/decryption utilities
            from app.utils.file_utils import encrypt_file, decrypt_file, generate_unique_filename, get_mime_type
            
            # Test encryption
            encrypted_data = encrypt_file(test_file_content)
            print("✅ File encryption successful")
            
            # Test decryption
            decrypted_data = decrypt_file(encrypted_data)
            assert decrypted_data == test_file_content, "Decryption failed - data mismatch"
            print("✅ File decryption successful")
            
            # Test filename generation
            unique_filename = generate_unique_filename("test_file.txt")
            print(f"✅ Generated unique filename: {unique_filename}")
            
            # Test MIME type detection
            mime_type = get_mime_type("test_file.txt")
            print(f"✅ Detected MIME type: {mime_type}")
            
            # Test File model
            new_file = File(
                filename=unique_filename,
                original_filename="test_file.txt",
                encrypted_path=temp_file_path,
                file_size=len(test_file_content),
                mime_type=mime_type,
                owner_id=test_user.id
            )
            
            db.session.add(new_file)
            db.session.commit()
            
            print(f"✅ Created file record: {new_file.original_filename}")
            print(f"   - File size: {new_file.formatted_size}")
            print(f"   - Owner: {new_file.owner.username}")
            
            # Test access log
            log_entry = AccessLog(
                action='upload',
                user_id=test_user.id,
                file_id=new_file.id
            )
            
            db.session.add(log_entry)
            db.session.commit()
            
            print("✅ Created access log entry")
            
            # Test relationships
            user_files = test_user.files.all()
            assert len(user_files) == 1, "User files relationship failed"
            print(f"✅ User has {len(user_files)} file(s)")
            
            file_logs = new_file.access_logs.all()
            assert len(file_logs) == 1, "File access logs relationship failed"
            print(f"✅ File has {len(file_logs)} access log(s)")
            
            # Test file sharing
            new_file.is_shared = True
            db.session.commit()
            print("✅ File sharing toggle successful")
            
            # Test download count
            new_file.download_count += 1
            db.session.commit()
            print(f"✅ Download count updated: {new_file.download_count}")
            
            print("\n🎉 All file operation tests passed!")
            
        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
            # Clean up database
            User.query.filter_by(username='testfileuser').delete()
            db.session.commit()
            print("🧹 Test cleanup completed")

def test_web_routes():
    """Test file-related web routes"""
    print("\nTesting Web Routes")
    print("=" * 20)
    
    app = create_app()
    
    with app.test_client() as client:
        # Test upload page (should redirect to login)
        response = client.get('/upload')
        print(f"Upload page (not logged in): Status {response.status_code}")
        assert response.status_code == 302, "Should redirect to login"
        
        # Test files page (should redirect to login)
        response = client.get('/files')
        print(f"Files page (not logged in): Status {response.status_code}")
        assert response.status_code == 302, "Should redirect to login"
        
        print("✅ Route protection working correctly")

if __name__ == '__main__':
    print("SecureShare File Functionality Tests")
    print("=" * 40)
    
    try:
        test_file_operations()
        test_web_routes()
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
