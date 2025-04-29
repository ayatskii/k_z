/**
 * Main JavaScript for Kazakh Learning website
 */

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });

    // Handle audio playback for word pronunciation
    const audioButtons = document.querySelectorAll('.pronunciation-btn');
    audioButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const audioId = this.getAttribute('data-audio-id');
            const audioElement = document.getElementById(audioId);
            
            if (audioElement) {
                audioElement.play();
            }
        });
    });

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Theme switching for non-logged in users
    // Check if user is not authenticated (no data-bs-theme attribute set by Django)
    const htmlElement = document.documentElement;
    
    if (!htmlElement.hasAttribute('data-bs-theme') || htmlElement.getAttribute('data-bs-theme') === "") {
        // Apply theme from localStorage if available
        const savedTheme = localStorage.getItem('site-theme') || 'light';
        
        // If previously saved black theme, default to dark
        const finalTheme = savedTheme === 'black' ? 'dark' : savedTheme;
        
        htmlElement.setAttribute('data-bs-theme', finalTheme);
        
        // Update active state in theme switcher
        updateActiveThemeIndicator(finalTheme);
    }
    
    // Add event listeners to theme switchers for non-logged in users
    const themeSwitchers = document.querySelectorAll('.theme-switcher');
    themeSwitchers.forEach(switcher => {
        switcher.addEventListener('click', function(e) {
            e.preventDefault();
            const targetTheme = this.getAttribute('data-theme');
            
            // Update HTML element attribute
            htmlElement.setAttribute('data-bs-theme', targetTheme);
            
            // Save to localStorage
            localStorage.setItem('site-theme', targetTheme);
            
            // Update active state
            updateActiveThemeIndicator(targetTheme);
        });
    });
    
    // Handle language switching with AJAX for smoother experience
    document.querySelectorAll('.language-switcher').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Extract language code from href
            const langHref = this.getAttribute('href');
            const langMatch = langHref.match(/\/language\/([a-z]{2})\//);
            
            if (langMatch && langMatch[1]) {
                const targetLang = langMatch[1];
                
                // Get CSRF token from meta tag
                const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
                
                // Add current URL as next parameter
                const currentUrl = window.location.pathname + window.location.search;
                const urlWithNext = `${langHref}?next=${encodeURIComponent(currentUrl)}`;
                
                // Show loading indicator
                const loadingToast = showToast('Changing language...', 'info');
                
                // Send AJAX request to change language server-side
                fetch(urlWithNext, {
                    method: 'GET',
                    headers: {
                        'X-CSRFToken': csrfToken || '',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    },
                    credentials: 'same-origin'
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Store the selected language
                        localStorage.setItem('site-language', targetLang);
                        
                        // Update the HTML lang attribute
                        document.documentElement.lang = targetLang;
                        
                        // Hide loading indicator
                        if (loadingToast) {
                            loadingToast.hide();
                        }
                        
                        // Show success message
                        showToast(data.message || 'Language changed successfully', 'success');
                        
                        // Force redirect to the specific URL with correct language prefix
                        setTimeout(() => {
                            if (data.redirect_url) {
                                // Ensure the URL has the correct language prefix
                                window.location.href = data.redirect_url;
                            } else {
                                // If no redirect URL provided, manually construct the URL with language prefix
                                const currentPath = window.location.pathname;
                                // Remove any existing language prefix
                                let newPath = currentPath;
                                const langPrefixMatch = currentPath.match(/^\/([a-z]{2})(\/|$)/);
                                if (langPrefixMatch) {
                                    newPath = currentPath.substring(langPrefixMatch[0].length);
                                    if (!newPath.startsWith('/')) {
                                        newPath = '/' + newPath;
                                    }
                                }
                                // Add the new language prefix
                                window.location.href = '/' + targetLang + newPath + window.location.search;
                            }
                        }, 500);
                    } else {
                        throw new Error(data.message || 'Language change failed');
                    }
                })
                .catch(error => {
                    console.error('Error changing language:', error);
                    
                    // Hide loading indicator
                    if (loadingToast) {
                        loadingToast.hide();
                    }
                    
                    // Show error message
                    showToast('Failed to change language. Please try again.', 'error');
                    
                    // Reload the page after a delay
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                });
            }
        });
    });
    
    // Update language indicators
    updateLanguageIndicators();
});

// Update active state on theme switchers
function updateActiveThemeIndicator(activeTheme) {
    // Remove active class from all switchers
    document.querySelectorAll('.theme-switcher').forEach(el => {
        el.classList.remove('active');
        
        // If this is the active theme, add active class
        if (el.getAttribute('data-theme') === activeTheme) {
            el.classList.add('active');
        }
    });
}

// Update active state on language switchers
function updateLanguageIndicators() {
    // Get current language from HTML lang attribute or localStorage
    let currentLang = document.documentElement.lang || 
                     localStorage.getItem('site-language') || 
                     'ru';  // Default to Russian
    
    // Update all the language links
    document.querySelectorAll('.language-switcher').forEach(el => {
        // Extract language code from href
        const langHref = el.getAttribute('href');
        const langMatch = langHref.match(/\/language\/([a-z]{2})\//);
        
        if (langMatch && langMatch[1]) {
            const linkLang = langMatch[1];
            
            // Add/remove active class based on current language
            if (linkLang === currentLang) {
                el.classList.add('active');
            } else {
                el.classList.remove('active');
            }
        }
    });
}

// Helper function to show toast messages
function showToast(message, type = 'info') {
    // Check if Bootstrap's toast is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        // Create toast element
        const toastEl = document.createElement('div');
        toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        // Add to container or body
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        toastContainer.appendChild(toastEl);
        
        // Initialize and show toast
        const toast = new bootstrap.Toast(toastEl, {
            animation: true,
            autohide: true,
            delay: 3000
        });
        toast.show();
        
        return toast;
    }
    return null;
} 