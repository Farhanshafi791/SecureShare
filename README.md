# SecureShare

A secure file sharing platform built with Flask that allows users to upload, encrypt, and share files safely.

## Features

- 🔐 **Secure Authentication** - User registration and login with password hashing
- 👥 **Role-based Access Control** - Admin and user roles with different permissions
- 📁 **File Management** - Upload, store, and share files securely (Coming Soon)
- 🔒 **Encryption** - All files are encrypted before storage (Coming Soon)
- 📊 **Admin Dashboard** - User management and system monitoring
- 🔍 **Access Logging** - Track all file operations for security (Coming Soon)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```

### 3. Access the Application
Open your browser and go to: `http://localhost:5000`

## Project Structure

```
SecureShare/
├── app/                     # Main application package
│   ├── models/             # Database models
│   ├── auth/               # Authentication blueprint
│   ├── main/               # Main application blueprint
│   ├── admin/              # Admin panel blueprint
│   ├── static/             # Static files (CSS, JS, images)
│   └── templates/          # Jinja2 templates
├── scripts/                # Utility scripts
├── tests/                  # Test files
├── docs/                   # Documentation
├── instance/               # Instance-specific files
├── config.py               # Configuration
├── run.py                  # Application entry point
└── requirements.txt        # Dependencies
```

## User Management

### Create Admin User
```bash
python scripts/create_admin.py
```

### View All Users
```bash
python scripts/check_db.py
```

### Admin Web Interface
1. Login as admin at `/auth/login`
2. Go to `/admin/dashboard`
3. Click "User Management" to view all users

## Development

### Run Tests
```bash
python -m pytest tests/
```

### Database Migration
```bash
python scripts/migrate_db.py
```

## Security Features

- ✅ Password hashing using Werkzeug
- ✅ Session management with Flask-Login
- ✅ CSRF protection (Coming Soon)
- ✅ Role-based access control
- ✅ Secure file storage (Coming Soon)

## License

This project is open source. See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
