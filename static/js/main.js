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