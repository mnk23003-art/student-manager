// ==========================================
// Theme Management
// ==========================================
function initTheme() {
    const saved = localStorage.getItem('sm-theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
    } else {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }
    updateThemeIcon();
}

function updateThemeIcon() {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    const theme = document.documentElement.getAttribute('data-theme');
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('sm-theme', next);
    updateThemeIcon();
}

function toggleThemeAndSave() {
    toggleTheme();
    const theme = document.documentElement.getAttribute('data-theme');
    fetch('/accounts/set-theme/' + theme + '/', { method: 'GET', credentials: 'same-origin' });
}

// ==========================================
// Language Management
// ==========================================
function toggleLanguage() {
    const current = '{{ LANGUAGE_CODE|default:"en" }}';
    const next = current === 'ru' ? 'en' : 'ru';
    window.location.href = '/accounts/set-language/' + next + '/';
}

// ==========================================
// Mobile Menu
// ==========================================
function toggleMobileMenu() {
    const overlay = document.getElementById('mobileMenuOverlay');
    const sheet = document.getElementById('mobileMenuSheet');
    if (overlay && sheet) {
        overlay.classList.toggle('show');
        sheet.classList.toggle('show');
        document.body.style.overflow = sheet.classList.contains('show') ? 'hidden' : '';
    }
}

function closeMobileMenu() {
    const overlay = document.getElementById('mobileMenuOverlay');
    const sheet = document.getElementById('mobileMenuSheet');
    if (overlay && sheet) {
        overlay.classList.remove('show');
        sheet.classList.remove('show');
        document.body.style.overflow = '';
    }
}

// ==========================================
// User Menu
// ==========================================
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

// ==========================================
// Quick Add Menu
// ==========================================
function toggleQuickAdd() {
    const menu = document.getElementById('quickAddMenu');
    if (menu) {
        menu.classList.toggle('show');
        if (menu.classList.contains('show')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
}

// ==========================================
// Toast Notifications
// ==========================================
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer') || createToastContainer();

    const icons = {
        success: 'fa-circle-check',
        error: 'fa-circle-xmark',
        warning: 'fa-triangle-exclamation',
        info: 'fa-circle-info',
        danger: 'fa-circle-xmark'
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-icon"><i class="fas ${icons[type] || icons.info}"></i></div>
        <div class="toast-content"><p class="toast-message">${message}</p></div>
        <button class="toast-close" onclick="this.closest('.toast').remove()"><i class="fas fa-xmark"></i></button>
    `;

    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add('toast-show');
    });

    setTimeout(() => {
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hide');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function initToasts() {
    const toasts = document.querySelectorAll('[data-auto-dismiss]');
    toasts.forEach((toast, index) => {
        setTimeout(() => {
            toast.classList.add('toast-show');
        }, index * 100);

        setTimeout(() => {
            toast.classList.add('toast-hide');
            setTimeout(() => toast.remove(), 300);
        }, 4000 + index * 100);
    });
}

// ==========================================
// Confirmation Dialog
// ==========================================
function showConfirmDialog(message, actionUrl, confirmText = 'Удалить') {
    let dialog = document.getElementById('confirmDialog');
    if (!dialog) {
        dialog = createConfirmDialog();
    }

    dialog.querySelector('.modal-body p').textContent = message;
    dialog.querySelector('form').action = actionUrl;
    dialog.querySelector('.btn-danger').textContent = confirmText;
    dialog.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeConfirmDialog() {
    const dialog = document.getElementById('confirmDialog');
    if (dialog) {
        dialog.classList.remove('show');
        document.body.style.overflow = '';
    }
}

function createConfirmDialog() {
    const overlay = document.createElement('div');
    overlay.id = 'confirmDialog';
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">Подтвердите действие</h3>
                <button class="modal-close-btn" onclick="closeConfirmDialog()"><i class="fas fa-xmark"></i></button>
            </div>
            <div class="modal-body"><p></p></div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeConfirmDialog()">Отмена</button>
                <form method="post" style="display:inline"><button type="submit" class="btn btn-danger">Удалить</button></form>
            </div>
        </div>
    `;
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeConfirmDialog();
    });
    document.body.appendChild(overlay);
    return overlay;
}

// ==========================================
// Click Outside Handlers
// ==========================================
function initClickOutside() {
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.user-menu-wrapper')) {
            const dropdown = document.getElementById('userDropdown');
            if (dropdown) dropdown.classList.remove('show');
        }

        if (!e.target.closest('.quick-add-trigger') && !e.target.closest('.quick-add-menu')) {
            const menu = document.getElementById('quickAddMenu');
            if (menu && menu.classList.contains('show')) {
                toggleQuickAdd();
            }
        }

        if (!e.target.closest('.search-bar-wrapper')) {
            const results = document.getElementById('searchResults');
            if (results) results.classList.remove('show');
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeConfirmDialog();
            const menu = document.getElementById('quickAddMenu');
            if (menu && menu.classList.contains('show')) toggleQuickAdd();
            const dropdown = document.getElementById('userDropdown');
            if (dropdown) dropdown.classList.remove('show');
            const results = document.getElementById('searchResults');
            if (results) results.classList.remove('show');
        }
    });
}

// ==========================================
// Global Search
// ==========================================
let searchTimeout = null;

function initGlobalSearch() {
    const input = document.getElementById('globalSearch');
    const results = document.getElementById('searchResults');
    if (!input || !results) return;

    input.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        const query = input.value.trim();
        if (query.length < 2) {
            results.classList.remove('show');
            results.innerHTML = '';
            return;
        }

        searchTimeout = setTimeout(() => {
            fetch('/core/search/?q=' + encodeURIComponent(query), {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(r => r.text())
            .then(html => {
                results.innerHTML = html;
                results.classList.add('show');
            });
        }, 250);
    });

    input.addEventListener('focus', () => {
        if (results.innerHTML.trim()) results.classList.add('show');
    });
}

// ==========================================
// Pomodoro Timer
// ==========================================
let focusTimer = null;
let focusDurationSec = 25 * 60;
let focusRemaining = 0;
let focusInterval = null;
let focusSessionId = null;
let focusRunning = false;

function initFocusTimer() {
    const sel = document.getElementById('focusDurationSelect');
    if (sel) {
        focusDurationSec = parseInt(sel.value) * 60;
        focusRemaining = focusDurationSec;
        updateFocusDisplay();
        updateFocusProgress();
    }
    const circumference = 2 * Math.PI * 45;
    const prog = document.getElementById('timer-progress');
    if (prog) {
        prog.style.strokeDasharray = circumference;
        prog.style.strokeDashoffset = 0;
    }
}

function onDurationChange(el) {
    if (focusRunning) return;
    focusDurationSec = parseInt(el.value) * 60;
    focusRemaining = focusDurationSec;
    updateFocusDisplay();
    updateFocusProgress();
}

function updateFocusDisplay() {
    const display = document.getElementById('timer-display');
    if (!display) return;
    const mins = Math.floor(focusRemaining / 60);
    const secs = focusRemaining % 60;
    display.textContent = String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
}

function updateFocusProgress() {
    const prog = document.getElementById('timer-progress');
    if (!prog) return;
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (focusRemaining / focusDurationSec) * circumference;
    prog.style.strokeDashoffset = offset;
}

function startFocusTimer() {
    if (focusRunning) return;
    focusRunning = true;
    updateFocusButtons();

    fetch('/productivity/start/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ task_id: null }),
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) focusSessionId = data.session_id;
    })
    .catch(() => {});

    focusInterval = setInterval(() => {
        focusRemaining--;
        updateFocusDisplay();
        updateFocusProgress();
        if (focusRemaining <= 0) {
            completeFocusTimer();
        }
    }, 1000);
}

function pauseFocusTimer() {
    if (!focusRunning) return;
    clearInterval(focusInterval);
    focusRunning = false;
    updateFocusButtons();
}

function resumeFocusTimer() {
    if (focusRunning || focusRemaining <= 0) return;
    focusRunning = true;
    updateFocusButtons();
    focusInterval = setInterval(() => {
        focusRemaining--;
        updateFocusDisplay();
        updateFocusProgress();
        if (focusRemaining <= 0) {
            completeFocusTimer();
        }
    }, 1000);
}

function stopFocusTimer() {
    clearInterval(focusInterval);
    focusRunning = false;
    if (focusSessionId) {
        fetch('/productivity/' + focusSessionId + '/stop/', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).catch(() => {});
        focusSessionId = null;
    }
    focusRemaining = focusDurationSec;
    updateFocusDisplay();
    updateFocusProgress();
    updateFocusButtons();
}

function resetFocusTimer() {
    clearInterval(focusInterval);
    focusRunning = false;
    focusRemaining = focusDurationSec;
    focusSessionId = null;
    updateFocusDisplay();
    updateFocusProgress();
    updateFocusButtons();
}

function completeFocusTimer() {
    clearInterval(focusInterval);
    focusRunning = false;
    if (focusSessionId) {
        fetch('/productivity/' + focusSessionId + '/stop/', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
        }).catch(() => {});
        focusSessionId = null;
    }
    showToast('Сессия завершена! Отличная работа!', 'success');
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Сессия завершена!', { body: 'Отличная работа! Время для отдыха.' });
    }
    focusRemaining = focusDurationSec;
    updateFocusDisplay();
    updateFocusProgress();
    updateFocusButtons();
}

function updateFocusButtons() {
    const start = document.getElementById('startBtn');
    const pause = document.getElementById('pauseBtn');
    const stop = document.getElementById('stopBtn');
    if (!start) return;
    if (focusRunning) {
        start.style.display = 'none';
        pause.style.display = '';
        pause.innerHTML = '<i class="fas fa-pause"></i> Пауза';
        pause.onclick = pauseFocusTimer;
        stop.style.display = '';
    } else {
        start.style.display = '';
        pause.style.display = 'none';
        stop.style.display = 'none';
    }
}

// ==========================================
// CSRF Token Helper
// ==========================================
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, val] = cookie.trim().split('=');
        if (key === name) return val;
    }
    return '';
}

// ==========================================
// Tab Switching
// ==========================================
function switchTab(tabId, container) {
    const scope = container || document;
    const tabs = scope.querySelectorAll('.tab-item');
    const contents = scope.querySelectorAll('.tab-content');

    tabs.forEach(tab => tab.classList.remove('active'));
    contents.forEach(content => content.classList.remove('active'));

    const targetTab = scope.querySelector(`[data-tab="${tabId}"]`);
    const targetContent = document.getElementById(tabId);

    if (targetTab) targetTab.classList.add('active');
    if (targetContent) targetContent.classList.add('active');
}

// ==========================================
// Keyboard Shortcuts
// ==========================================
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('globalSearch');
            if (searchInput) searchInput.focus();
        }

        if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
            e.preventDefault();
            toggleQuickAdd();
        }
    });
}

// ==========================================
// Page Load Animation (no flicker)
// ==========================================
function initPageAnimation() {
    // Removed opacity animation to prevent flickering
}

// ==========================================
// Smooth Progress Bar Animation
// ==========================================
function animateProgressBars() {
    document.querySelectorAll('.progress-fill').forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0';
        requestAnimationFrame(() => {
            setTimeout(() => {
                bar.style.transition = 'width 600ms ease';
                bar.style.width = targetWidth;
            }, 200);
        });
    });
}

// ==========================================
// Stagger Animation for Cards
// ==========================================
function initStaggerAnimation() {
    document.querySelectorAll('.animate-in').forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(12px)';
        setTimeout(() => {
            el.style.transition = 'opacity 400ms cubic-bezier(0.16, 1, 0.3, 1), transform 400ms cubic-bezier(0.16, 1, 0.3, 1)';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 60 + i * 40);
    });
}

// ==========================================
// Initialize
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initClickOutside();
    initToasts();
    initPageAnimation();
    initKeyboardShortcuts();
    initGlobalSearch();
    initFocusTimer();

    setTimeout(animateProgressBars, 400);
    setTimeout(initStaggerAnimation, 50);
});

// HTMX Configuration
document.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = getCookie('csrftoken');
});

document.addEventListener('htmx:afterRequest', (event) => {
    if (event.detail.successful) {
        const trigger = event.detail.requestConfig?.trigger;
        if (trigger === 'task-completed') {
            showToast('Задача выполнена!', 'success');
        }
    }
});
