import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import secrets
import base64
import hashlib


def generate_aes_key_from_password(password, salt):
    """Generate AES key from password using PBKDF2"""
    return PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)


def get_encryption_key():
    """Get the encryption key from config"""
    from config import Config
    # Use a fixed salt for consistency (in production, use environment variable)
    salt = hashlib.sha256(Config.ENCRYPTION_KEY.encode()).digest()[:16]
    return generate_aes_key_from_password(Config.ENCRYPTION_KEY.encode(), salt)


def encrypt_file_aes(file_data):
    """Encrypt file data using AES-256-CBC"""
    # Generate a random initialization vector (IV)
    iv = get_random_bytes(16)  # 16 bytes for AES
    
    # Get the encryption key
    key = get_encryption_key()
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the data to be multiple of 16 bytes (AES block size)
    padding_length = 16 - (len(file_data) % 16)
    padded_data = file_data + bytes([padding_length] * padding_length)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)
    
    # Combine IV and encrypted data
    return iv + encrypted_data


def decrypt_file_aes(encrypted_data):
    """Decrypt file data using AES-256-CBC"""
    # Extract IV (first 16 bytes)
    iv = encrypted_data[:16]
    encrypted_content = encrypted_data[16:]
    
    # Get the encryption key
    key = get_encryption_key()
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt the data
    padded_data = cipher.decrypt(encrypted_content)
    
    # Remove padding
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]


# Wrapper functions to maintain compatibility with existing code
def encrypt_file(file_data):
    """Encrypt file data using AES encryption"""
    return encrypt_file_aes(file_data)


def decrypt_file(encrypted_data):
    """Decrypt file data using AES encryption"""
    return decrypt_file_aes(encrypted_data)


def allowed_file(filename, allowed_extensions):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_unique_filename(original_filename):
    """Generate a unique filename to prevent conflicts"""
    # Get file extension
    name, ext = os.path.splitext(secure_filename(original_filename))
    # Generate unique identifier
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Return unique filename
    return f"{name}_{timestamp}_{unique_id}{ext}"


def get_file_path(upload_folder, filename):
    """Get the full file path"""
    return os.path.join(upload_folder, filename)


def ensure_upload_directory(upload_folder):
    """Ensure the upload directory exists"""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)


def get_file_size(file_path):
    """Get file size in bytes"""
    return os.path.getsize(file_path)


def delete_file(file_path):
    """Safely delete a file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception:
        pass
    return False


def get_mime_type(filename):
    """Get MIME type based on file extension"""
    import mimetypes
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'application/octet-stream'


def is_audio_file(filename):
    """Check if the file is an audio file based on extension"""
    audio_extensions = {'mp3', 'wav', 'flac', 'ogg', 'aac', 'm4a', 'wma', 'aiff', 'au'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in audio_extensions


def is_image_file(filename):
    """Check if the file is an image file based on extension"""
    image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in image_extensions


def is_document_file(filename):
    """Check if the file is a document file based on extension"""
    document_extensions = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in document_extensions


def get_file_category(filename):
    """Get the category of the file based on its extension"""
    if is_audio_file(filename):
        return 'audio'
    elif is_image_file(filename):
        return 'image'
    elif is_document_file(filename):
        return 'document'
    else:
        return 'other'


def get_file_icon_class(filename):
    """Get the appropriate Font Awesome icon class for the file type"""
    category = get_file_category(filename)
    
    if category == 'audio':
        return 'fas fa-music'
    elif category == 'image':
        return 'fas fa-image'
    elif category == 'document':
        return 'fas fa-file-alt'
    elif filename.rsplit('.', 1)[1].lower() in {'zip', 'rar', '7z', 'tar', 'gz'}:
        return 'fas fa-file-archive'
    else:
        return 'fas fa-file'
