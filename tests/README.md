# Tests Directory - Comprehensive Test Suite

This directory contains the complete test suite for the SecureShare application, ensuring code quality, security, and reliability.

## 📁 Test Structure

```
tests/
├── 📄 conftest.py                    # Pytest configuration & fixtures
├── 📄 test_app.py                   # Application factory tests
├── 📄 test_auth.py                  # Authentication & authorization
├── 📄 test_models.py                # Database model tests
├── 📄 test_admin.py                 # Admin panel functionality
├── 📄 test_file_functionality.py   # File operations & sharing
├── 📄 test_email.py                 # Email system tests
├── 📄 test_encryption.py           # Security & encryption tests
├── 📄 test_home.py                  # Home page & navigation
└── 📄 README.md                     # This documentation
```

## 🧪 Test Categories

### 🔧 Core Application Tests

#### `test_app.py` - Application Factory
- Flask app creation and configuration
- Extension initialization (SQLAlchemy, Flask-Login, Flask-Mail)
- Blueprint registration verification
- Environment-specific configuration testing

#### `test_models.py` - Database Models
- **User Model**: Authentication, roles, relationships
- **File Model**: Metadata, encryption info, sharing settings
- **AccessLog Model**: Activity tracking, audit trails
- **ContactMessage Model**: Support system integration
- Database constraints and validation

### 🔐 Authentication & Security Tests

#### `test_auth.py` - Authentication System
- User registration with email verification
- Login/logout functionality
- Password hashing with bcrypt
- Role-based access control (admin/user)
- Session management
- Password reset workflows

#### `test_encryption.py` - Security Features
- AES-256 encryption implementation
- File encryption/decryption cycles
- Key management and security
- Edge cases and error handling
- Performance under load

### 📁 Feature-Specific Tests

#### `test_file_functionality.py` - File Operations
- **Upload Process**: File validation, size limits, type restrictions
- **Encryption**: Automatic encryption on upload
- **Storage**: Secure file storage and retrieval
- **Sharing**: Token generation, access control, expiration
- **Download**: Decryption and secure delivery
- **Metadata**: File information tracking

#### `test_admin.py` - Administrative Features
- Admin dashboard functionality
- User management (create, view, delete, modify)
- System statistics and monitoring
- File oversight and management
- Access control enforcement
- Audit log analysis

#### `test_email.py` - Email System
- **SMTP Configuration**: Connection and authentication
- **Email Templates**: Verification, notifications, alerts
- **Sending Process**: Queue handling, error recovery
- **Verification**: Email verification workflows
- **Notifications**: File sharing notifications

#### `test_home.py` - Navigation & UI
- Home page functionality
- Navigation menu testing
- Responsive design elements
- User dashboard features
- Template rendering

### 🎧 Support System Tests
- Contact form functionality
- Help system integration
- User feedback collection
- Support ticket management

## 🔧 Test Configuration

### `conftest.py` - Test Setup
Contains essential pytest fixtures and configuration:

- **`app` fixture**: Clean Flask application instance
- **`client` fixture**: Test client for HTTP requests
- **`db` fixture**: Fresh database for each test
- **`user` fixture**: Test user creation
- **`admin_user` fixture**: Admin user for privilege testing
- **Database cleanup**: Automatic teardown after tests

## 🚀 Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test Categories
```bash
# Authentication tests
pytest tests/test_auth.py

# File functionality tests  
pytest tests/test_file_functionality.py

# Security/encryption tests
pytest tests/test_encryption.py

# Admin panel tests
pytest tests/test_admin.py
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

## 📊 Test Coverage Goals

### Current Coverage Areas
- ✅ **Authentication**: Login, registration, password security
- ✅ **File Operations**: Upload, encryption, sharing, download
- ✅ **Database Models**: All models and relationships
- ✅ **Admin Functions**: User management, system monitoring
- ✅ **Email System**: Sending, templates, verification
- ✅ **Security**: Encryption, access control, validation

### Coverage Targets
- **Minimum**: 80% code coverage
- **Goal**: 90%+ code coverage
- **Critical paths**: 100% coverage for security functions

## 🛡️ Security Testing

### Encryption Tests
- AES-256 implementation validation
- Key generation and management
- File encryption/decryption integrity
- Performance under various file sizes

### Access Control Tests
- Role-based permission enforcement
- File ownership validation
- Share link security
- Admin privilege separation

### Input Validation Tests
- SQL injection prevention
- XSS protection
- File upload validation
- Form input sanitization

## 🔄 Continuous Integration

### Test Automation
- Automated test execution on code changes
- Coverage reporting and tracking
- Performance regression detection
- Security vulnerability scanning

### Test Database
- Isolated test database for each test run
- Automatic schema creation and cleanup
- Test data factory patterns
- Database transaction rollback

## 📋 Writing New Tests

### Test Organization
1. **Group by functionality**: Keep related tests together
2. **Use descriptive names**: Test function names should explain the scenario
3. **Test edge cases**: Include boundary conditions and error cases
4. **Mock external services**: Use mocking for email, file system operations

### Test Patterns
```python
def test_feature_success_case():
    """Test the happy path for feature X"""
    # Arrange
    # Act
    # Assert

def test_feature_error_handling():
    """Test error handling for feature X"""
    # Test various error conditions

def test_feature_edge_cases():
    """Test boundary conditions for feature X"""
    # Test limits, empty inputs, etc.
```

### Best Practices
- **Isolation**: Each test should be independent
- **Cleanup**: Use fixtures for setup and teardown
- **Assertions**: Use clear, specific assertions
- **Documentation**: Include docstrings explaining test purpose

## ⚠️ Important Notes

- **Test Database**: Tests use a separate SQLite database that's created and destroyed for each test run
- **File System**: Temporary directories are used for file upload tests
- **Email**: Email sending is mocked in tests to prevent actual email delivery
- **Environment**: Tests run in a special testing configuration
- **Isolation**: Each test is completely isolated from others

## 🔍 Debugging Tests

### Common Issues
- **Database State**: Ensure proper cleanup between tests
- **File Permissions**: Check temporary file creation permissions
- **Mock Objects**: Verify mocks are properly configured
- **Environment Variables**: Ensure test environment is properly set

### Debugging Commands
```bash
# Run single test with debug output
pytest tests/test_auth.py::test_login -v -s

# Run with pdb debugger
pytest tests/test_auth.py::test_login --pdb

# Show test output
pytest tests/ -s
```

This comprehensive test suite ensures the reliability, security, and maintainability of the SecureShare platform.

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=app --cov-report=html
```

## Test Coverage

The test suite covers:
- ✅ User authentication and authorization
- ✅ Password hashing and verification
- ✅ File upload and encryption (AES-256)
- ✅ Database models and relationships
- ✅ Email functionality
- ✅ Admin panel operations
- ✅ Support system and contact forms
- ✅ Utility functions
- ✅ Security features and edge cases
- ✅ Error handling and validation

## Test Database

Tests use a separate in-memory SQLite database that is created and destroyed for each test session to ensure test isolation and fast execution.

## Writing New Tests

When adding new features, ensure to:
1. Add corresponding unit tests
2. Test both success and failure scenarios
3. Include edge cases and validation tests
4. Maintain test isolation using fixtures
5. Follow the existing naming conventions

## Test Organization

### Unit Tests
Focus on testing individual components in isolation:
- `test_models.py` - Database model validation
- `test_auth.py` - Authentication logic
- Individual AES test files

### Integration Tests  
Test component interactions:
- `test_complete.py` - Full application workflow
- `test_file_functionality.py` - File upload/download flow

### Utility Tests
Test external dependencies and configurations:
- `test_email.py` - Email system configuration
- `test_pycryptodome.py` - Encryption library setup

## Writing New Tests

When adding new test files:
1. Follow the naming convention: `test_<feature>.py`
2. Import required fixtures from `conftest.py`
3. Use descriptive test function names: `test_<action>_<expected_result>`
4. Include both positive and negative test cases
5. Add appropriate docstrings and comments

## Best Practices

- **Isolation**: Each test should be independent
- **Cleanup**: Use fixtures for setup/teardown
- **Assertions**: Use specific assertions with clear error messages
- **Data**: Use test-specific data, avoid production data
- **Performance**: Keep tests fast and focused
