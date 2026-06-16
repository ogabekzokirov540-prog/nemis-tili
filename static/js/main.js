/**
 * GermanMaster AI - Main JavaScript
 * Umumiy funksiyalar va utility'lar
 */

// CSRF Token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        info: 'bg-blue-600',
        warning: 'bg-yellow-600',
    };

    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300 translate-x-full`;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => notification.classList.remove('translate-x-full'), 10);

    // Auto remove
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Audio player utility
function playAudioFile(url) {
    const audio = new Audio(url);
    audio.play().catch(err => {
        console.warn('Audio play failed:', err);
        showNotification('Audio o\'ynab bo\'lmadi', 'error');
    });
}

// Text-to-Speech (browser built-in)
function speakGerman(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'de-DE';
        utterance.rate = 0.8;
        speechSynthesis.speak(utterance);
    } else {
        showNotification('Brauzeringiz nutq sintezini qo\'llab-quvvatlamaydi', 'warning');
    }
}

// Debounce utility
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

// Local storage utilities for progress
const ProgressStorage = {
    getStudyStart() {
        return localStorage.getItem('study_start');
    },
    
    startStudy() {
        if (!this.getStudyStart()) {
            localStorage.setItem('study_start', Date.now());
        }
    },
    
    getStudyMinutes() {
        const start = this.getStudyStart();
        if (!start) return 0;
        return Math.round((Date.now() - parseInt(start)) / 60000);
    },
    
    resetStudy() {
        localStorage.removeItem('study_start');
    }
};

// Auto-start study timer
document.addEventListener('DOMContentLoaded', function() {
    ProgressStorage.startStudy();

    // Page animations
    const content = document.querySelector('main');
    if (content) {
        content.classList.add('page-transition');
    }
});

// Keyboard shortcuts info
console.log(`
🇩🇪 GermanMaster AI - Keyboard Shortcuts:
- Ctrl+K: Global search
- Space/Enter: Flip flashcard
- 1-4: Rate flashcard (after flip)
`);
