# App Directory - SecureShare Core Application

This directory contains the main Flask application code organized in a modular blueprint structure.

## 📁 Directory Structure

```
app/
├── 📂 admin/              # Admin panel functionality
├── 📂 auth/               # Authentication & user management
├── 📂 main/               # Core file sharing features
├── 📂 support/            # Support & contact system
├── 📂 models/             # Database models
├── 📂 utils/              # Utility functions
├── 📂 static/             # Frontend assets
├── 📂 templates/          # HTML templates
└── 📄 __init__.py         # Flask app factory
```

## 🔧 Core Components

### `__init__.py` - Application Factory
- **Flask App Creation**: Uses the factory pattern for flexible app configuration
- **Extension Initialization**: Sets up SQLAlchemy, Flask-Login, Flask-Mail
- **Blueprint Registration**: Connects all modular components
- **Security Configuration**: Configures CSRF protection and security headers

### Blueprints Overview

#### 🔐 **auth/** - Authentication System
- User registration with email verification
- Secure login/logout with bcrypt password hashing
- Role-based access control (admin/user)
- Password reset functionality

#### 📁 **main/** - File Sharing Core
- File upload with AES-256 encryption
- Secure file storage and retrieval
- Share link generation with token-based access
- User dashboard and file management

#### 👥 **admin/** - Administrative Panel
- User management (view, delete, modify)
- System statistics and monitoring
- File oversight and management
- Access log analysis

#### 🎧 **support/** - Support System
- Contact form handling
- Help documentation
- User feedback collection

### 🗄️ **models/** - Database Schema
Contains SQLAlchemy models defining the database structure:
- **User**: User accounts, roles, authentication
- **File**: File metadata, encryption info, sharing settings
- **AccessLog**: Audit trail for all file operations
- **ContactMessage**: Support system messages

### 🛠️ **utils/** - Utility Functions
Helper modules for common operations:
- **file_utils.py**: File handling, encryption, validation
- **email_utils.py**: Email sending, templates, verification
- **security_utils.py**: Token generation, validation, security headers

### 🎨 **static/** - Frontend Assets
```
static/
├── css/           # Stylesheets (modern-ui.css)
├── js/            # JavaScript (modern-ui.js)
└── images/        # Icons, logos, graphics
```

### 📄 **templates/** - HTML Templates
Jinja2 templates organized by blueprint:
```
templates/
├── base.html           # Base template with common layout
├── admin/             # Admin panel templates
├── auth/              # Login, register, verification templates  
├── main/              # Dashboard, file management templates
└── support/           # Contact, help templates
```

## 🔐 Security Features

- **AES-256 Encryption**: All uploaded files encrypted at rest
- **CSRF Protection**: Prevents cross-site request forgery
- **Secure Headers**: XSS protection, content type sniffing prevention
- **Input Validation**: Comprehensive form validation and sanitization
- **Access Control**: Role-based permissions and file ownership checks

## 🚀 Key Features

1. **Secure File Upload**: Encrypted storage with metadata tracking
2. **Share Management**: Token-based file sharing with access controls
3. **User Dashboard**: Intuitive file management interface
4. **Admin Tools**: Comprehensive user and system management
5. **Audit Logging**: Complete activity tracking for security

## 📊 Database Models

### User Model
- Authentication (username, email, password hash)
- Role management (admin/user)
- Email verification status
- File ownership relationships

### File Model
- Original filename and encrypted storage path
- File metadata (size, type, upload time)
- Sharing configuration (tokens, permissions)
- Download tracking

### AccessLog Model
- User activity tracking
- File operation logging
- Timestamp and action recording
- Security audit trail

## 🔄 Application Flow

1. **User Registration** → Email verification → Account activation
2. **File Upload** → Encryption → Database entry → Storage
3. **File Sharing** → Token generation → Access link creation
4. **File Access** → Token validation → Decryption → Download
5. **Admin Oversight** → User management → System monitoring

This modular structure ensures maintainability, security, and scalability for the SecureShare platform.
