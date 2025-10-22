class ChatBot {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.initializeEventListeners();
        this.setWelcomeTime();
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    initializeEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Input focus effects
        this.messageInput.addEventListener('focus', () => {
            this.messageInput.parentElement.style.transform = 'scale(1.02)';
        });

        this.messageInput.addEventListener('blur', () => {
            this.messageInput.parentElement.style.transform = 'scale(1)';
        });
    }

    setWelcomeTime() {
        const welcomeTimeElement = document.getElementById('welcomeTime');
        if (welcomeTimeElement) {
            welcomeTimeElement.textContent = this.formatTime(new Date());
        }
    }

    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Disable input while processing
        this.setInputState(false);
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send message to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response to chat
            this.addMessage(data.response, 'bot');
            
            // Update session ID if provided
            if (data.session_id) {
                this.sessionId = data.session_id;
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot', true);
        } finally {
            // Re-enable input
            this.setInputState(true);
        }
    }

    addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = `message-avatar ${sender}-avatar`;
        
        if (sender === 'bot') {
            avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
        } else {
            avatarDiv.innerHTML = '<i class="fas fa-user"></i>';
        }
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = text;
        
        if (isError) {
            textDiv.style.background = 'linear-gradient(135deg, #e74c3c, #c0392b)';
        }
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date());
        
        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(timeDiv);
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        
        if (enabled) {
            this.messageInput.focus();
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    async loadHistory() {
        try {
            const response = await fetch(`/history/${this.sessionId}`);
            if (response.ok) {
                const data = await response.json();
                // Process history if needed
                console.log('History loaded:', data.history);
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }
}

// Global function for suggestion buttons
function sendSuggestion(message) {
    const chatBot = window.chatBotInstance;
    if (chatBot) {
        chatBot.messageInput.value = message;
        chatBot.sendMessage();
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatBotInstance = new ChatBot();
    
    // Add some interactive effects
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    suggestionBtns.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add loading animation to send button
    const sendButton = document.getElementById('sendButton');
    sendButton.addEventListener('click', () => {
        sendButton.style.animation = 'pulse 0.3s ease-in-out';
        setTimeout(() => {
            sendButton.style.animation = '';
        }, 300);
    });
});

// Add CSS animation for pulse effect
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);
