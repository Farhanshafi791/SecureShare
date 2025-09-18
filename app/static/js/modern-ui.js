/**
 * SecureShare Modern UI JavaScript
 * Enhanced user interactions and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize drag and drop for file uploads
    initializeDragAndDrop();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize tooltips and popovers
    initializeBootstrapComponents();
    
    // Initialize theme toggle
    initializeThemeToggle();
    
    // Initialize progress bars
    initializeProgressBars();
});

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Copied to clipboard!', 'success');
    }
}

/**
 * Show loading state on button
 */
function showButtonLoading(button, text = 'Loading...') {
    if (!button) return;
    
    // Store original state
    if (!button.dataset.originalText) {
        button.dataset.originalText = button.innerHTML;
        button.dataset.originalDisabled = button.disabled;
    }
    
    button.disabled = true;
    const spinner = button.querySelector('.loading-spinner');
    if (spinner) {
        spinner.classList.remove('d-none');
    } else {
        button.innerHTML = `<span class="loading-spinner me-2"></span>${text}`;
    }
}

/**
 * Hide loading state on button
 */
function hideButtonLoading(button) {
    if (!button) return;
    
    if (button.dataset.originalText) {
        button.innerHTML = button.dataset.originalText;
        button.disabled = button.dataset.originalDisabled === 'true';
        delete button.dataset.originalText;
        delete button.dataset.originalDisabled;
    }
}

/**
 * Initialize scroll animations and entrance effects
 */
function initializeAnimations() {
    // Fade in elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate
    document.querySelectorAll('.feature-card, .stats-card, .card').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Initialize drag and drop functionality for file uploads
 */
function initializeDragAndDrop() {
    const dropZones = document.querySelectorAll('.file-upload-area');
    
    dropZones.forEach(dropZone => {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        // Handle dropped files
        dropZone.addEventListener('drop', handleDrop, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        e.currentTarget.classList.add('dragover');
    }
    
    function unhighlight(e) {
        e.currentTarget.classList.remove('dragover');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            const fileInput = document.querySelector('input[type="file"]');
            if (fileInput) {
                fileInput.files = files;
                updateFileInputDisplay(files);
            }
        }
    }
}

/**
 * Update file input display with selected files
 */
function updateFileInputDisplay(files) {
    const fileList = document.querySelector('.file-list');
    if (!fileList) return;
    
    fileList.innerHTML = '';
    
    Array.from(files).forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item d-flex align-items-center justify-content-between p-3 border rounded mb-2';
        fileItem.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-file text-primary me-3"></i>
                <div>
                    <div class="fw-medium">${file.name}</div>
                    <small class="text-muted">${formatFileSize(file.size)}</small>
                </div>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger remove-file" data-index="${index}">
                <i class="fas fa-times"></i>
            </button>
        `;
        fileList.appendChild(fileItem);
    });
    
    // Add remove file functionality
    document.querySelectorAll('.remove-file').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.file-item').remove();
        });
    });
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Initialize form enhancements
 */
function initializeFormEnhancements() {
    // Auto-resize textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
    
    // Add floating labels
    document.querySelectorAll('.form-control').forEach(input => {
        if (input.placeholder) {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });
        }
    });
    
    // Initialize form submission handling with loading states
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            
            if (submitBtn) {
                // Check form validity first
                if (!this.checkValidity()) {
                    // Don't show loading for invalid forms
                    hideButtonLoading(submitBtn);
                    return;
                }
                
                showButtonLoading(submitBtn, 'Processing...');
                
                // Auto-reset after reasonable timeout, but prioritize page navigation
                let timeoutId = setTimeout(() => {
                    if (document.contains(submitBtn)) {
                        hideButtonLoading(submitBtn);
                    }
                }, 3000); // Increased to 3 seconds for form processing
                
                // Clear timeout if the page starts unloading (form submission successful)
                window.addEventListener('beforeunload', () => {
                    clearTimeout(timeoutId);
                }, { once: true });
            }
        });
        
        // Handle form reset events
        form.addEventListener('reset', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                hideButtonLoading(submitBtn);
            }
        });
        
        // Handle form validation events
        form.addEventListener('invalid', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                hideButtonLoading(submitBtn);
            }
        }, true);
    });
    
    // Enhanced file input styling
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            updateFileInputDisplay(this.files);
        });
    });
    
    // Initialize password toggles
    initializePasswordToggles();
}

/**
 * Initialize password toggle functionality
 */
function initializePasswordToggles() {
    // Handle all password toggle buttons
    document.querySelectorAll('[id^="toggle"]').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.id.replace('toggle', '').toLowerCase();
            let targetInput;
            
            // Find the associated input field
            if (targetId === 'password') {
                targetInput = document.getElementById('password');
            } else if (targetId === 'confirmpassword') {
                targetInput = document.getElementById('confirm_password');
            }
            
            if (targetInput) {
                const icon = this.querySelector('i');
                
                if (targetInput.type === 'password') {
                    targetInput.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    targetInput.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });
}

/**
 * Setup password toggle for specific button and input IDs (legacy function for template compatibility)
 */
function setupPasswordToggle(buttonId, inputId) {
    const button = document.getElementById(buttonId);
    const input = document.getElementById(inputId);
    
    if (button && input) {
        button.addEventListener('click', function() {
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    }
}

/**
 * Initialize Bootstrap components
 */
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Initialize theme toggle functionality
 */
function initializeThemeToggle() {
    const themeToggle = document.querySelector('#themeToggle');
    if (!themeToggle) return;
    
    // Get saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
}

/**
 * Initialize animated progress bars
 */
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.style.width || bar.getAttribute('aria-valuenow') + '%';
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.id = toastId;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${getToastIcon(type)} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1080';
    document.body.appendChild(container);
    return container;
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle',
        'primary': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Add smooth scrolling to anchor links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Expose utility functions globally
window.SecureShare = {
    showToast,
    showButtonLoading,
    hideButtonLoading,
    copyToClipboard,
    formatFileSize
};
