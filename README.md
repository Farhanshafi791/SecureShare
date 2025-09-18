# SecureShare

A secure file sharing platform built with Flask that allows users to upload, encrypt, and share files safely with enterprise-grade security features.

## 🚀 Features

- 🔐 **Secure Authentication** - User registration, login with bcrypt password hashing, and email verification
- 👥 **Role-based Access Control** - Admin and user roles with granular permissions
- 📁 **Advanced File Management** - Upload, store, and share files with metadata tracking
- 🔒 **AES-256 Encryption** - Military-grade encryption for all stored files
- 📊 **Comprehensive Admin Dashboard** - User management, system monitoring, and analytics
- 🔍 **Security Audit Logging** - Track all file operations and user activities
- 🌐 **Secure File Sharing** - Generate time-limited, password-protected sharing links
- 📧 **Email Integration** - Automated verification and notification system
- 🎵 **Multi-format Support** - Support for documents, images, audio, and video files

## 📁 Project Structure

```
SecureShare/
├── 📂 app/                      # Main Flask application (see app/README.md)
│   ├── 📂 admin/               # Admin panel functionality
│   ├── 📂 auth/                # Authentication & user management
│   ├── 📂 main/                # Core file sharing features
│   ├── 📂 support/             # Support & contact system
│   ├── 📂 models/              # Database models
│   ├── 📂 utils/               # Utility functions
│   ├── 📂 static/              # Frontend assets (CSS, JS, images)
│   ├── 📂 templates/           # Jinja2 HTML templates
│   └── 📄 __init__.py          # Flask app factory
├── 📂 scripts/                 # Maintenance & utility scripts (see scripts/README.md)
│   ├── 📂 admin/              # Administrative utilities
│   ├── 📂 database/           # Database operations & migrations
│   └── 📂 setup/              # Initial setup & configuration
├── 📂 tests/                   # Comprehensive test suite (see tests/README.md)
├── 📂 instance/                # Instance-specific files (database)
├── 📂 uploads/                 # Encrypted user files
├── 📄 config.py               # Application configuration
├── 📄 run.py                  # Application entry point
└── 📄 requirements.txt        # Python dependencies
```

## 📚 Documentation

Documentation is now organized within each directory:

- **`app/README.md`** - Complete application architecture and component details
- **`scripts/README.md`** - Maintenance scripts, database migrations, and admin utilities
- **`tests/README.md`** - Test suite organization, coverage, and testing guidelines
- **`config.py`** - Application configuration and environment settings
- **`requirements.txt`** - Python dependencies and versions
## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/Farhanshafi791/SecureShare.git
cd SecureShare
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
# See scripts/README.md for detailed script documentation
python scripts/database/migrate_db.py
```

### 4. Create Admin User
```bash
# See scripts/README.md for all admin utilities
python scripts/admin/create_admin.py
```

### 5. Run the Application
```bash
python run.py
```

### 6. Access the Application
- **User Interface**: `http://localhost:5000`
- **Admin Panel**: `http://localhost:5000/admin` (login as admin)

## 📖 Documentation

Each directory contains detailed README files:

- 📁 [`app/README.md`](app/README.md) - Application architecture and components
- 📁 [`tests/README.md`](tests/README.md) - Testing strategy and coverage
- 📁 [`scripts/README.md`](scripts/README.md) - Utility scripts documentation
- 📁 [`docs/README.md`](docs/README.md) - Complete documentation index

For detailed setup and usage instructions, see [`docs/00_Quick_Start_Guide.md`](docs/00_Quick_Start_Guide.md).

## 🛠️ Development

### Testing
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_auth.py tests/test_models.py

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Database Management
```bash
# Check database status
python scripts/admin/check_db.py

# View users
python scripts/admin/view_users.py

# Database migrations
python scripts/database/migrate_db.py

# Reset database (⚠️ Destructive)
python scripts/database/reset_database.py
```

### Email Configuration
```bash
# Setup email server
python scripts/setup/setup_email.py
```

## 🔒 Security Features

- ✅ **Encryption**: AES-256 file encryption with unique keys
- ✅ **Authentication**: Bcrypt password hashing + email verification
- ✅ **Authorization**: Role-based access control (Admin/User)
- ✅ **Session Security**: Secure session management with Flask-Login
- ✅ **Audit Trail**: Comprehensive access logging and monitoring
- ✅ **Secure Sharing**: Time-limited, password-protected share links
- ✅ **Input Validation**: SQL injection and XSS prevention
- ✅ **File Security**: Type validation and malware scanning

## 📖 Additional Documentation

For detailed information about specific components:

- **Application Architecture**: See `app/README.md` for complete Flask application structure
- **Maintenance Scripts**: See `scripts/README.md` for database operations and admin utilities  
- **Testing Guide**: See `tests/README.md` for comprehensive testing information
- **Configuration**: Check `config.py` for environment settings and security keys

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework and community
- Contributors and testers
- Security research community
