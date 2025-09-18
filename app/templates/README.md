# Templates Directory

This directory contains all Jinja2 HTML templates for the SecureShare application's user interface.

## Template Structure

### Base Templates

- **`base.html`** - Main base template with common layout, navigation, and styling
- **`layout.html`** - Extended layout template for specific page structures

### Authentication Templates

- **`auth/`** - Authentication-related templates
  - `login.html` - User login form
  - `register.html` - User registration form
  - `verify_email.html` - Email verification page
  - `reset_password.html` - Password reset functionality

### Main Application Templates

- **`main/`** - Core application templates
  - `index.html` - Home page and file upload interface
  - `dashboard.html` - User dashboard with file management
  - `share.html` - File sharing interface
  - `download.html` - File download page

### Administrative Templates

- **`admin/`** - Admin panel templates
  - `dashboard.html` - Admin dashboard overview
  - `users.html` - User management interface
  - `files.html` - File management interface
  - `logs.html` - System logs and audit trail

### Support Templates

- **`support/`** - Support and contact templates
  - `contact.html` - Contact form
  - `help.html` - Help and documentation pages

### Utility Templates

- **`errors/`** - Error page templates
  - `404.html` - Page not found
  - `500.html` - Internal server error
  - `403.html` - Access forbidden

- **`email/`** - Email templates
  - `verification.html` - Email verification template
  - `password_reset.html` - Password reset email template

## Template Features

- **Responsive Design**: Bootstrap-based responsive layout
- **Security**: CSRF protection and XSS prevention
- **Accessibility**: WCAG compliant markup
- **Internationalization**: Ready for multi-language support
- **Component Reuse**: Modular template components and macros

## Styling

Templates use Bootstrap 5 for responsive design and custom CSS for application-specific styling. All templates extend the base template for consistent layout and navigation.
