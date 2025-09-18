# Utils Directory

This directory contains utility functions and helper modules used throughout the SecureShare application.

## Utility Modules

### Communication

- **`email_utils.py`** - Email sending and verification utilities
  - SMTP configuration and connection handling
  - Email template rendering
  - Verification email sending
  - Password reset email functionality
  - Error handling and retry logic

### File Management

- **`file_utils.py`** - File upload, encryption, and processing utilities
  - Secure file upload handling
  - AES-256 encryption/decryption
  - File type validation and security checks
  - Thumbnail generation for images
  - File size and format validation
  - Storage path management

### Security

- **`password_utils.py`** - Password hashing and validation utilities
  - Bcrypt password hashing
  - Password strength validation
  - Secure password generation
  - Hash verification
  - Salt generation and management

### User Interface

- **`ui_utils.py`** - UI helper functions and template utilities
  - Flash message helpers
  - Form validation helpers
  - Template context processors
  - Date/time formatting utilities
  - File size formatting
  - User-friendly error messages

### Configuration

- **`__init__.py`** - Utility function exports and module initialization

## Design Principles

- **Separation of Concerns**: Each utility module handles a specific domain
- **Reusability**: Functions are designed to be used across multiple components
- **Security**: All utilities implement security best practices
- **Error Handling**: Comprehensive error handling and logging
- **Testing**: All utilities are fully unit tested

## Usage

Import utilities as needed throughout the application:

```python
from app.utils.email_utils import send_verification_email
from app.utils.file_utils import encrypt_file
from app.utils.password_utils import hash_password
from app.utils.ui_utils import format_file_size
```
