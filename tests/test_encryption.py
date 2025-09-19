#!/usr/bin/env python3
"""
AES encryption tests for SecureShare application
"""

import sys
import traceback
from unittest.mock import Mock

# Add the project root to the Python path
sys.path.append('.')

# --- Mocks needed for testing before actual imports ---
# This mock is necessary because the file_utils import a Config object
# that might not be configured when running this test standalone.
class MockConfig:
    ENCRYPTION_KEY = 'x9KtyAddCOCQlmjGJK4DtleWhCFy3mgSThwMjmxDPbE'

# Mock the config module before importing any app utilities that depend on it
sys.modules['config'] = Mock()
sys.modules['config'].Config = MockConfig

# --- Actual imports from the application ---
from app.utils.file_utils import encrypt_file, decrypt_file

def run_aes_encryption_tests():
    """Execute all tests for the AES encryption/decryption utilities"""
    print("Testing AES Encryption & Decryption")
    print("=" * 40)

    # --- Test 1: Basic Round-Trip ---
    print("\nTesting basic AES encryption and decryption...")
    test_data_basic = b"Hello, this is a test file content for AES encryption!"
    encrypted_basic = encrypt_file(test_data_basic)
    
    assert encrypted_basic is not None, "Encryption returned None"
    assert encrypted_basic != test_data_basic, "Encrypted data is the same as original data"
    assert len(encrypted_basic) > len(test_data_basic), "Encrypted data should be larger due to IV and padding"
    
    decrypted_basic = decrypt_file(encrypted_basic)
    assert decrypted_basic == test_data_basic, "Basic decryption failed - data mismatch"
    print("✅ Basic encryption and decryption round-trip successful")

    # --- Test 2: Empty Data ---
    print("\nTesting AES encryption with empty data...")
    test_data_empty = b""
    encrypted_empty = encrypt_file(test_data_empty)
    assert encrypted_empty is not None
    
    decrypted_empty = decrypt_file(encrypted_empty)
    assert decrypted_empty == test_data_empty, "Empty data decryption failed"
    print("✅ Encryption of empty data successful")

    # --- Test 3: Large Data (1MB) ---
    print("\nTesting AES encryption with large data (1MB)...")
    test_data_large = b"A" * (1024 * 1024)  # 1MB of data
    encrypted_large = encrypt_file(test_data_large)
    assert encrypted_large is not None
    
    decrypted_large = decrypt_file(encrypted_large)
    assert decrypted_large == test_data_large, "Large data decryption failed"
    print("✅ Encryption of large data successful")

    # --- Test 4: Unicode Data ---
    print("\nTesting AES encryption with unicode data...")
    test_data_unicode = "Hello 🌍 Unicode test with émojis and spéciål chäractêrs! 🔒".encode('utf-8')
    encrypted_unicode = encrypt_file(test_data_unicode)
    assert encrypted_unicode is not None
    
    decrypted_unicode = decrypt_file(encrypted_unicode)
    assert decrypted_unicode == test_data_unicode, "Unicode data decryption failed"
    print("✅ Encryption of unicode data successful")

    # --- Test 5: Different Data Sizes ---
    print("\nTesting AES encryption with various data sizes...")
    sizes = [1, 15, 16, 17, 64, 256, 1024, 4096]
    for size in sizes:
        test_data_sized = b"X" * size
        encrypted_sized = encrypt_file(test_data_sized)
        assert encrypted_sized is not None
        decrypted_sized = decrypt_file(encrypted_sized)
        assert decrypted_sized == test_data_sized, f"Decryption failed for data size: {size}"
    print("✅ Encryption successful across multiple data sizes")

    # --- Test 6: Reproducibility Check ---
    print("\nTesting that encryption is non-deterministic (due to random IV)...")
    test_data_repro = b"Test data for reproducibility check"
    encrypted1 = encrypt_file(test_data_repro)
    encrypted2 = encrypt_file(test_data_repro)
    
    assert encrypted1 != encrypted2, "Encryption produced identical results, which is incorrect for CBC with random IV"
    print("✅ Encryption produces different ciphertext each time")
    
    assert decrypt_file(encrypted1) == test_data_repro
    assert decrypt_file(encrypted2) == test_data_repro
    print("✅ Both ciphertexts decrypt to the same original data")

    print("\n🎉 All AES encryption tests passed!")

if __name__ == '__main__':
    print("SecureShare AES Encryption Tests")
    print("=" * 40)
    
    try:
        run_aes_encryption_tests()
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)