"""
Utility function tests for SecureShare application
"""

from app.utils.password_utils import hash_password, verify_password
from app.utils.file_utils import get_file_extension, is_allowed_file
from app.utils.ui_utils import format_file_size


def test_password_utilities():
    """Test password hashing and verification utilities"""
    password = "testpassword123"
    
    # Test password hashing
    hashed = hash_password(password)
    assert hashed is not None
    assert hashed != password  # Should be hashed, not plain text
    
    # Test password verification
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_file_utilities():
    """Test file utility functions"""
    # Test file extension detection
    assert get_file_extension("test.txt") == "txt"
    assert get_file_extension("document.pdf") == "pdf"
    assert get_file_extension("image.jpg") == "jpg"
    assert get_file_extension("noextension") == ""
    
    # Test allowed file types
    assert is_allowed_file("document.pdf") is True
    assert is_allowed_file("image.jpg") is True
    assert is_allowed_file("text.txt") is True
    assert is_allowed_file("malicious.exe") is False


def test_ui_utilities():
    """Test UI utility functions"""
    # Test file size formatting
    assert format_file_size(1024) == "1.0 KB"
    assert format_file_size(1048576) == "1.0 MB"
    assert format_file_size(1073741824) == "1.0 GB"
    assert format_file_size(500) == "500 B"


def test_file_size_edge_cases():
    """Test file size formatting edge cases"""
    assert format_file_size(0) == "0 B"
    assert format_file_size(1) == "1 B"
    assert format_file_size(1023) == "1023 B"
