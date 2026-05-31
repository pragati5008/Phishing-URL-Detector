// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    // URL validation
    const urlInput = document.getElementById('urlInput');
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            validateUrl(this);
        });
    }
    
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
    
    // Add copy functionality
    const urlDisplay = document.querySelector('.url-display p');
    if (urlDisplay) {
        urlDisplay.addEventListener('click', function() {
            copyToClipboard(this.textContent);
        });
    }
    
    // Load history from localStorage
    loadHistoryFromStorage();
});

function validateUrl(input) {
    const urlPattern = /^https?:\/\/.+\..+/;
    if (urlPattern.test(input.value)) {
        input.style.borderColor = '#50c878';
    } else {
        input.style.borderColor = '#e74c3c';
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('URL copied to clipboard!');
    }).catch(() => {
        showToast('Failed to copy URL');
    });
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--dark-color);
        color: white;
        padding: 1rem;
        border-radius: var(--border-radius);
        animation: slideIn 0.3s ease;
        z-index: 9999;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function loadHistoryFromStorage() {
    const historyList = document.querySelector('.history-list');
    if (historyList && !historyList.children.length) {
        const storedHistory = JSON.parse(localStorage.getItem('phishHistory') || '[]');
        
        if (storedHistory.length > 0) {
            historyList.innerHTML = '';
            storedHistory.forEach(item => {
                addHistoryItem(item);
            });
        }
    }
}

function addHistoryItem(item) {
    const historyList = document.querySelector('.history-list');
    if (!historyList) return;
    
    const historyItem = document.createElement('div');
    historyItem.className = `history-item ${item.result}`;
    historyItem.innerHTML = `
        <div class="history-icon">
            <i class="fas fa-link"></i>
        </div>
        <div class="history-details">
            <div class="history-url">${item.url}</div>
            <div class="history-meta">
                <span class="history-result ${item.result}">
                    <i class="fas ${item.result === 'phishing' ? 'fa-exclamation-triangle' : 'fa-check-circle'}"></i>
                    ${item.result.charAt(0).toUpperCase() + item.result.slice(1)}
                </span>
                <span class="history-confidence">
                    <i class="fas fa-chart-line"></i> Confidence: ${item.confidence}
                </span>
                <span class="history-time">
                    <i class="fas fa-clock"></i> ${item.timestamp || 'Just now'}
                </span>
            </div>
        </div>
    `;
    
    historyList.prepend(historyItem);
}

// Add loading animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .toast {
        box-shadow: var(--box-shadow);
    }
    
    .url-display p {
        cursor: pointer;
        transition: opacity 0.3s ease;
    }
    
    .url-display p:hover {
        opacity: 0.8;
    }
    
    .url-display p:active {
        transform: scale(0.98);
    }
`;

document.head.appendChild(style);