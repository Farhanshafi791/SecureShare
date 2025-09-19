#!/usr/bin/env python3
"""
Utility function tests for SecureShare application
"""

import sys
import traceback
from unittest.mock import Mock

# Add the project root to the Python path
sys.path.append('.')

# --- Mocks needed for testing before actual imports ---
class MockConfig:
    ENCRYPTION_KEY = 'a_secure_and_long_test_encryption_key_for_aes'

# Mock the config module before importing any app utilities that might need it
sys.modules['config'] = Mock()
sys.modules['config'].Config = MockConfig

# --- Actual imports from the application ---
from wtforms import ValidationError
# Adjusting import based on your provided file structure
from app.utils.password_utils import validate_password_complexity, check_password_strength
from app.utils.file_utils import (
    encrypt_file,
    decrypt_file,
    allowed_file,
    generate_unique_filename,
    get_mime_type,
    get_file_category,
    get_file_icon_class
)

def run_all_utility_tests():
    """Execute all tests for the utility functions"""
    print("Testing All Utility Functions")
    print("=" * 30)

    # --- Test 1: Password Validation and Strength Utilities ---
    print("\nTesting Password Utilities...")

    # Test the WTForms password complexity validator
    try:
        mock_field = Mock(data='StrongP@ss1')
        validate_password_complexity(None, mock_field)
        print("✅ Password validator correctly accepts a valid password")

        # Test failing conditions
        fail_scenarios = {
            'Short1@': 'Password must be at least 8 characters long.',
            'weakpass1@': 'Password must contain at least one uppercase letter.',
            'WEAKPASS1@': 'Password must contain at least one lowercase letter.',
            'WeakPass@': 'Password must contain at least one number.',
            # --- THIS IS THE CORRECTED LINE ---
            'WeakPass1': 'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>).',
        }
        
        for password, expected_msg in fail_scenarios.items():
            mock_field.data = password
            try:
                validate_password_complexity(None, mock_field)
                # This line should not be reached if the validator works correctly
                raise AssertionError(f"Validator failed to reject invalid password: {password}")
            except ValidationError as e:
                # Assert that the captured exception's message is exactly what we expect
                assert str(e) == expected_msg, f"For password '{password}', expected message '{expected_msg}' but got '{str(e)}'"
        print("✅ Password validator correctly rejects invalid passwords")

    except Exception as e:
        print(f"❌ Test failed during password validation: {e}")
        raise

    # Test the password strength checker
    strong_result = check_password_strength('StrongP@ss1')
    assert strong_result['score'] == 5
    assert strong_result['strength'] == 'Strong'
    assert not strong_result['feedback']
    print("✅ Password strength checker identifies a strong password")
    
    weak_result = check_password_strength('weak')
    assert weak_result['score'] == 1
    assert weak_result['strength'] == 'Very Weak'
    assert "At least 8 characters" in weak_result['feedback']
    assert "One uppercase letter" in weak_result['feedback']
    assert "One number" in weak_result['feedback']
    print("✅ Password strength checker identifies a weak password with correct feedback")

    # --- Test 2: File Encryption and Decryption Utilities ---
    print("\nTesting File Encryption Utilities...")
    
    original_data = b"This is a top secret message for testing AES encryption."
    encrypted_data = encrypt_file(original_data)
    assert encrypted_data is not None and original_data not in encrypted_data
    print("✅ File encryption successful")
    
    decrypted_data = decrypt_file(encrypted_data)
    assert decrypted_data == original_data, "Decryption failed - data mismatch"
    print("✅ File decryption successful (round-trip test passed)")
    
    # --- Test 3: General File Utilities ---
    print("\nTesting General File Utilities...")

    allowed_extensions = {'txt', 'pdf', 'png'}
    assert allowed_file('document.txt', allowed_extensions) is True
    assert allowed_file('image.PNG', allowed_extensions) is True
    assert allowed_file('archive.zip', allowed_extensions) is False
    print("✅ Allowed file extension check is correct")
    
    unique_name = generate_unique_filename('my_file.jpg')
    assert 'my_file' in unique_name and unique_name.endswith('.jpg') and unique_name != 'my_file.jpg'
    print("✅ Unique filename generation is correct")

    assert get_mime_type('test.pdf') == 'application/pdf'
    assert get_mime_type('unknown.xyz') == 'application/octet-stream'
    print("✅ MIME type detection is correct")

    assert get_file_category('song.mp3') == 'audio'
    assert get_file_category('photo.jpeg') == 'image'
    assert get_file_category('report.docx') == 'document'
    assert get_file_category('data.csv') == 'other'
    print("✅ File category detection is correct")

    assert get_file_icon_class('song.wav') == 'fas fa-music'
    assert get_file_icon_class('archive.zip') == 'fas fa-file-archive'
    assert get_file_icon_class('unknown.dat') == 'fas fa-file'
    print("✅ File icon class selection is correct")
    
    print("\n🎉 All utility function tests passed!")

if __name__ == '__main__':
    print("SecureShare Utility Tests")
    print("=" * 40)
    
    try:
        run_all_utility_tests()
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)