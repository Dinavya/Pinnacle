// ==================== Theme Toggle ====================
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;
const body = document.body;

// Load theme preference from localStorage
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        enableDarkMode();
    }
}

// Enable dark mode
function enableDarkMode() {
    body.classList.add('dark-mode');
    htmlElement.setAttribute('data-theme', 'dark');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    localStorage.setItem('theme', 'dark');
}

// Disable dark mode
function disableDarkMode() {
    body.classList.remove('dark-mode');
    htmlElement.setAttribute('data-theme', 'light');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    localStorage.setItem('theme', 'light');
}

// Toggle theme
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('dark-mode')) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    });
}

// Load theme on page load
loadTheme();

// ==================== Alert Messages ====================
const alertCloseButtons = document.querySelectorAll('.alert-close');
alertCloseButtons.forEach(button => {
    button.addEventListener('click', function() {
        const alert = this.closest('.alert');
        alert.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => alert.remove(), 300);
    });
});

// Auto-dismiss alerts after 5 seconds
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        if (alert) {
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => alert.remove(), 300);
        }
    }, 5000);
});

// ==================== Smooth Scroll ====================
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

// ==================== Navbar Scroll Effect ====================
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
    }
    
    lastScroll = currentScroll;
});

// ==================== Form Validation ====================
class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.validate(e));
        }
    }

    validate(e) {
        const inputs = this.form.querySelectorAll('[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showError(input, 'This field is required');
                isValid = false;
            } else if (input.type === 'email' && !this.isValidEmail(input.value)) {
                this.showError(input, 'Invalid email address');
                isValid = false;
            } else {
                this.clearError(input);
            }
        });

        if (!isValid) {
            e.preventDefault();
        }
        return isValid;
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    showError(input, message) {
        input.classList.add('input-error');
        let errorMsg = input.nextElementSibling;
        if (!errorMsg || !errorMsg.classList.contains('error-message')) {
            errorMsg = document.createElement('div');
            errorMsg.classList.add('error-message');
            input.parentNode.insertBefore(errorMsg, input.nextSibling);
        }
        errorMsg.textContent = message;
    }

    clearError(input) {
        input.classList.remove('input-error');
        const errorMsg = input.nextElementSibling;
        if (errorMsg && errorMsg.classList.contains('error-message')) {
            errorMsg.remove();
        }
    }
}

// ==================== Animation Observer ====================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all animatable elements
document.querySelectorAll('.feature-card, .job-card, .result-card').forEach(el => {
    observer.observe(el);
});

// ==================== Utility Functions ====================

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Capitalize first letter
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==================== Lazy Loading ====================
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ==================== Export Functions ====================

// Export data as CSV
function exportCSV(data, filename = 'data.csv') {
    let csv = '';
    const headers = Object.keys(data[0]);
    csv += headers.join(',') + '\n';

    data.forEach(row => {
        csv += headers.map(header => {
            const value = row[header];
            return typeof value === 'string' && value.includes(',') 
                ? `"${value}"` 
                : value;
        }).join(',') + '\n';
    });

    downloadFile(csv, filename, 'text/csv');
}

// Export data as JSON
function exportJSON(data, filename = 'data.json') {
    const json = JSON.stringify(data, null, 2);
    downloadFile(json, filename, 'application/json');
}

// Download file helper
function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

// ==================== Debounce & Throttle ====================

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ==================== Search Functionality ====================

class SearchManager {
    constructor(inputSelector, resultsSelector) {
        this.input = document.querySelector(inputSelector);
        this.resultsContainer = document.querySelector(resultsSelector);
        
        if (this.input) {
            this.input.addEventListener('input', debounce((e) => this.search(e), 300));
        }
    }

    async search(event) {
        const query = event.target.value.trim();
        
        if (query.length < 2) {
            this.resultsContainer.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            // Results will be rendered server-side
        } catch (error) {
            console.error('Search error:', error);
        }
    }
}

// ==================== Page Load ====================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Resume Parser App Loaded');
    
    // Initialize animations
    initializeAnimations();
    
    // Check if it's the home page and animate counter
    if (document.querySelector('.stat-number')) {
        animateCounters();
    }
    
    // Apply data-driven styles (widths, background colors) set via data- attributes in templates
    applyDataStyles();
});

// Set element styles from `data-width` and `data-bg` attributes to avoid inline Jinja in style attrs
function applyDataStyles() {
    document.querySelectorAll('[data-width]').forEach(el => {
        const val = el.dataset.width;
        if (val !== undefined && val !== null && val !== '') {
            el.style.width = String(val) + '%';
        }
    });

    document.querySelectorAll('[data-bg]').forEach(el => {
        const bg = el.dataset.bg;
        if (bg) el.style.background = bg;
    });
}

// ==================== Counter Animation ====================

function animateCounters() {
    const counters = document.querySelectorAll('[data-count]');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                const target = parseInt(entry.target.dataset.count);
                animateCounter(entry.target, target);
                entry.target.classList.add('counted');
            }
        });
    }, { threshold: 0.1 });

    counters.forEach(counter => counterObserver.observe(counter));
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 50;
    const updateCounter = () => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
        } else {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        }
    };
    updateCounter();
}

// ==================== Initialize Animations ====================

function initializeAnimations() {
    // Fade-in animation for elements
    const elements = document.querySelectorAll('[data-animate]');
    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('animate-fade-in');
                }, index * 100);
                animationObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(el => animationObserver.observe(el));
}

// Export functions globally
window.FormValidator = FormValidator;
window.SearchManager = SearchManager;
window.exportCSV = exportCSV;
window.exportJSON = exportJSON;
window.showNotification = showNotification;
window.copyToClipboard = copyToClipboard;