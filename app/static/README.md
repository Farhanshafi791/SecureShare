# Static Directory

This directory contains all static assets for the SecureShare application including CSS, JavaScript, images, and other frontend resources.

## Directory Structure

### Stylesheets (`css/`)
- **`style.css`** - Main application stylesheet
- **`admin.css`** - Admin panel specific styles
- **`auth.css`** - Authentication page styles
- **`responsive.css`** - Mobile and tablet responsive styles

### JavaScript (`js/`)
- **`main.js`** - Core application JavaScript functionality
- **`file-upload.js`** - File upload handling and progress bars
- **`share.js`** - File sharing interface interactions
- **`admin.js`** - Admin panel functionality
- **`security.js`** - Client-side security features

### Images (`img/`)
- **`logo.png`** - Application logo
- **`icons/`** - Application icons and favicons
- **`backgrounds/`** - Background images and patterns
- **`placeholders/`** - Placeholder images

### Fonts (`fonts/`)
- **Custom fonts** - Application-specific typography
- **Icon fonts** - Icon libraries and symbol fonts

### Vendor Libraries (`vendor/`)
- **Bootstrap** - CSS framework
- **jQuery** - JavaScript library
- **FontAwesome** - Icon library
- **Other third-party libraries**

## Features

### CSS Features
- **Responsive Design**: Mobile-first responsive layout
- **Custom Theming**: SecureShare brand colors and typography
- **Dark Mode Support**: Alternative color scheme
- **Accessibility**: High contrast and screen reader support

### JavaScript Features
- **Progressive Enhancement**: Works without JavaScript
- **File Upload**: Drag and drop file upload with progress
- **Form Validation**: Client-side form validation
- **Security**: CSRF token handling and XSS prevention

### Performance
- **Minification**: Compressed CSS and JavaScript files
- **Caching**: Proper cache headers for static assets
- **CDN Ready**: Optimized for content delivery networks
- **Lazy Loading**: Optimized image loading

## Usage

Static files are served by Flask and cached for performance. In production, these should be served by a web server like Nginx for optimal performance.
