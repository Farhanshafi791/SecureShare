# Models Directory

This directory contains all database models for the SecureShare application using SQLAlchemy ORM.

## Model Files

### Core Models

- **`user.py`** - User model with authentication features
  - User registration and login functionality
  - Email verification system
  - Password hashing with bcrypt
  - Admin role management
  - Account activation/deactivation

- **`file.py`** - File model with encryption and sharing capabilities
  - AES-256 file encryption
  - Secure file upload handling
  - Share link generation with expiration
  - Password-protected sharing
  - File access control

### Supporting Models

- **`access_log.py`** - Access logging for security auditing
  - User login/logout tracking
  - File access monitoring
  - IP address logging
  - Timestamp recording
  - Security event tracking

- **`contact_message.py`** - Contact form message model
  - Support ticket system
  - Message categorization
  - Response tracking
  - User communication history

### Configuration

- **`__init__.py`** - Model imports and database initialization
  - Database instance configuration
  - Model registration
  - Migration support setup

## Key Features

- **Security First**: All sensitive data is properly encrypted
- **Audit Trail**: Comprehensive logging for security monitoring
- **Relationships**: Proper foreign key relationships between models
- **Validation**: Built-in data validation and constraints
- **Migration Support**: Database schema versioning and updates

## Database Schema

The models create a normalized database schema with proper indexing for performance and foreign key constraints for data integrity. See `02_Database_Models.md` in the docs directory for detailed schema documentation.
