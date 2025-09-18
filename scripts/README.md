# Scripts Directory - Maintenance & Utility Tools

This directory contains maintenance scripts and utilities for managing the SecureShare application.

## 📁 Directory Structure

```
scripts/
├── 📂 admin/              # Administrative utilities
├── 📂 database/           # Database operations & migrations
├── 📂 setup/              # Initial setup & configuration
└── 📄 README.md           # This documentation
```

## 🗄️ Database Scripts (`/database/`)

### Migration Scripts
Essential for database schema management and upgrades:

- **`migrate_db.py`** - Main database migration coordinator
- **`migrate_contact_message.py`** - Contact system database migration
- **`migrate_email_verification.py`** - Email verification features migration
- **`migrate_file_functionality.py`** - File management features migration
- **`migrate_share_links.py`** - File sharing system migration
- **`migrate_to_aes.py`** - AES encryption system migration
- **`update_database_schema.py`** - General schema update utilities

### Database Utilities
- **`reset_database.py`** - ⚠️ **CAUTION**: Completely resets database
- **`backup_database.py`** - Create database backups
- **`verify_schema.py`** - Validate database integrity

## 👥 Admin Scripts (`/admin/`)

### User Management
- **`create_admin.py`** - Create administrator accounts
- **`clear_users.py`** - ⚠️ **CAUTION**: Remove user data
- **`view_users.py`** - Display user information
- **`debug_db.py`** - Database debugging utilities
- **`check_db.py`** - Database health checks

### System Maintenance
- **`cleanup_files.py`** - Remove orphaned files
- **`audit_system.py`** - Generate security audit reports
- **`check_permissions.py`** - Validate file permissions

## 🚀 Setup Scripts (`/setup/`)

### Initial Configuration
- **`setup_email.py`** - Configure and test email settings
- **`init_database.py`** - Initialize fresh database
- **`create_directories.py`** - Create required directory structure
- **`generate_keys.py`** - Generate encryption and secret keys

### Environment Setup
- **`install_dependencies.py`** - Install Python requirements
- **`check_environment.py`** - Validate system requirements
- **`configure_app.py`** - Initial application configuration

## 🔒 Security Considerations

### Before Running Scripts
1. **Backup**: Always backup your database before running migration scripts
2. **Environment**: Ensure you're running in the correct environment (dev/prod)
3. **Permissions**: Verify script has necessary file system permissions
4. **Configuration**: Check that config.py has correct settings

### Critical Scripts (Require Extra Caution)
- `reset_database.py` - **DESTRUCTIVE**: Deletes all data
- `clear_users.py` - **DESTRUCTIVE**: Removes user accounts
- `migrate_to_aes.py` - **IRREVERSIBLE**: Encrypts existing files
- `cleanup_files.py` - **PERMANENT**: Removes files from storage

## 📋 Usage Examples

### Create an Admin User
```bash
python scripts/admin/create_admin.py
```

### Run Database Migration
```bash
python scripts/database/migrate_db.py
```

### Reset Database (Development Only)
```bash
python scripts/database/reset_database.py --confirm
```

### Setup Fresh Installation
```bash
python scripts/setup/init_database.py
python scripts/setup/create_directories.py
python scripts/admin/create_admin.py
```

### Email Configuration
```bash
python scripts/setup/setup_email.py
```

## 🔧 Script Development Guidelines

### Creating New Scripts
1. **Location**: Place in appropriate subdirectory
2. **Documentation**: Include docstrings and comments
3. **Error Handling**: Implement proper exception handling
4. **Logging**: Use consistent logging format
5. **Confirmation**: Add confirmation prompts for destructive operations

### Testing Scripts
- Test in development environment first
- Use small datasets for validation
- Verify rollback procedures
- Document any prerequisites

## ⚠️ Important Notes

- **Production Use**: Always test scripts in development first
- **Backups**: Create backups before running any database scripts
- **Logs**: Check application logs after running scripts
- **Rollback**: Have rollback procedures ready for critical operations
- **Permissions**: Ensure proper file and database permissions
- **Run from Root**: All scripts should be executed from the project root directory

## 🔄 Common Workflows

### Fresh Installation
```bash
python scripts/setup/init_database.py
python scripts/setup/create_directories.py
python scripts/admin/create_admin.py
python scripts/setup/setup_email.py
```

### Database Migration
```bash
python scripts/database/migrate_db.py
```

### System Maintenance
```bash
python scripts/admin/check_db.py
python scripts/admin/cleanup_files.py
python scripts/admin/check_permissions.py
```

### User Management
```bash
python scripts/admin/view_users.py
python scripts/admin/create_admin.py
```

These scripts are essential for maintaining a healthy SecureShare installation and should be used with appropriate caution and preparation.
