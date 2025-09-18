"""
AES encryption tests for SecureShare application
"""

from app.utils.file_utils import encrypt_file, decrypt_file


def test_aes_encryption_basic():
    """Test basic AES encryption and decryption"""
    test_data = b"Hello, this is a test file content for AES encryption!"
    
    # Test encryption
    encrypted_data = encrypt_file(test_data)
    assert encrypted_data is not None
    assert encrypted_data != test_data
    assert len(encrypted_data) > len(test_data)  # Encrypted data should be larger
    
    # Test decryption
    decrypted_data = decrypt_file(encrypted_data)
    assert decrypted_data == test_data


def test_aes_encryption_empty_data():
    """Test AES encryption with empty data"""
    test_data = b""
    
    encrypted_data = encrypt_file(test_data)
    assert encrypted_data is not None
    
    decrypted_data = decrypt_file(encrypted_data)
    assert decrypted_data == test_data


def test_aes_encryption_large_data():
    """Test AES encryption with large data"""
    # Create 1MB of test data
    test_data = b"A" * (1024 * 1024)
    
    encrypted_data = encrypt_file(test_data)
    assert encrypted_data is not None
    
    decrypted_data = decrypt_file(encrypted_data)
    assert decrypted_data == test_data


def test_aes_encryption_unicode_data():
    """Test AES encryption with unicode data"""
    test_data = "Hello 🌍 Unicode test with émojis and spéciål chäractêrs! 🔒".encode('utf-8')
    
    encrypted_data = encrypt_file(test_data)
    assert encrypted_data is not None
    
    decrypted_data = decrypt_file(encrypted_data)
    assert decrypted_data == test_data


def test_aes_encryption_different_sizes():
    """Test AES encryption with different data sizes"""
    sizes = [1, 16, 64, 256, 1024, 4096]  # Test various sizes
    
    for size in sizes:
        test_data = b"X" * size
        
        encrypted_data = encrypt_file(test_data)
        assert encrypted_data is not None
        
        decrypted_data = decrypt_file(encrypted_data)
        assert decrypted_data == test_data


def test_aes_encryption_reproducibility():
    """Test that encryption produces different results each time (due to random IV)"""
    test_data = b"Test data for reproducibility check"
    
    encrypted1 = encrypt_file(test_data)
    encrypted2 = encrypt_file(test_data)
    
    # Should be different due to random IV
    assert encrypted1 != encrypted2
    
    # But both should decrypt to the same original data
    assert decrypt_file(encrypted1) == test_data
    assert decrypt_file(encrypted2) == test_data
