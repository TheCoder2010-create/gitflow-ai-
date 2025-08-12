// GitFlow AI Landing Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Terminal typing animation
    const terminalLines = document.querySelectorAll('.terminal-line .command');
    let currentLine = 0;

    function typeCommand(element, text, callback) {
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, 50);
            } else if (callback) {
                setTimeout(callback, 1000);
            }
        }
        type();
    }

    function startTerminalAnimation() {
        if (currentLine < terminalLines.length) {
            const line = terminalLines[currentLine];
            const originalText = line.textContent;
            typeCommand(line, originalText, () => {
                currentLine++;
                startTerminalAnimation();
            });
        } else {
            // Reset animation after 5 seconds
            setTimeout(() => {
                currentLine = 0;
                startTerminalAnimation();
            }, 5000);
        }
    }

    // Start terminal animation when hero section is visible
    const heroSection = document.querySelector('.hero');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                setTimeout(startTerminalAnimation, 1000);
                observer.unobserve(entry.target);
            }
        });
    });
    observer.observe(heroSection);

    // Floating elements animation
    function createFloatingElement() {
        const element = document.createElement('div');
        element.className = 'floating-element';
        
        // Random position
        element.style.left = Math.random() * 100 + '%';
        element.style.top = Math.random() * 100 + '%';
        
        // Random color
        const colors = ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        element.style.background = color;
        element.style.boxShadow = `0 0 20px ${color}50`;
        
        // Random animation duration
        element.style.animationDuration = (4 + Math.random() * 4) + 's';
        element.style.animationDelay = Math.random() * 2 + 's';
        
        document.querySelector('.floating-elements').appendChild(element);
        
        // Remove element after animation
        setTimeout(() => {
            element.remove();
        }, 8000);
    }

    // Create floating elements periodically
    setInterval(createFloatingElement, 2000);

    // Feature cards hover effect
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Button click animations
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(10, 10, 15, 0.98)';
        } else {
            navbar.style.background = 'rgba(10, 10, 15, 0.95)';
        }
    });

    // Parallax effect for hero background
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const heroBackground = document.querySelector('.hero-background');
        if (heroBackground) {
            heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });

    // Demo interactions - Make feature cards interactive
    const demoChats = document.querySelectorAll('.demo-chat');
    demoChats.forEach(chat => {
        chat.addEventListener('click', function() {
            // Extract the user question from the demo
            const userMessage = this.querySelector('.chat-message.user span');
            if (userMessage) {
                const question = userMessage.textContent;
                // Open AI chat with this question
                showAIChat();
                setTimeout(() => {
                    const chatInput = document.getElementById('chatInput');
                    if (chatInput) {
                        chatInput.value = question;
                        sendChatMessage();
                    }
                }, 500);
            }
        });
    });
    
    // Make other feature demos interactive
    const commitPreviews = document.querySelectorAll('.commit-preview');
    commitPreviews.forEach(preview => {
        preview.addEventListener('click', function() {
            showAIChat();
            setTimeout(() => {
                askQuickQuestion('Generate a commit message for my changes');
            }, 500);
        });
    });
    
    const workflowDiagrams = document.querySelectorAll('.workflow-diagram');
    workflowDiagrams.forEach(diagram => {
        diagram.addEventListener('click', function() {
            showAIChat();
            setTimeout(() => {
                askQuickQuestion('How do I merge my feature branch safely?');
            }, 500);
        });
    });
    
    const safetyAlerts = document.querySelectorAll('.safety-alert');
    safetyAlerts.forEach(alert => {
        alert.addEventListener('click', function() {
            showAIChat();
            setTimeout(() => {
                askQuickQuestion('What are the safety considerations for Git operations?');
            }, 500);
        });
    });

    // Intersection Observer for animations
    const animateOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    // Apply animation to feature cards
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        animateOnScroll.observe(card);
    });

    // Console welcome message
    console.log(`
    🤖 GitFlow AI - Welcome to the future of Git workflows!
    
    Built with ❤️ for the OpenAI Hackathon
    
    Features:
    • AI-powered Git assistance
    • Natural language commands
    • Smart commit messages
    • Workflow intelligence
    
    Ready to transform your Git experience?
    `);
});

// API Configuration
const API_BASE_URL = window.location.origin;

// Modal functions
function watchDemo() {
    document.getElementById('demoModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    loadDemoConversations();
}

function closeDemo() {
    document.getElementById('demoModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function startTrial() {
    // Show interactive AI chat instead of alert
    showAIChat();
}

// AI Chat Functions
function showAIChat() {
    // Create AI chat modal
    const chatModal = document.createElement('div');
    chatModal.id = 'aiChatModal';
    chatModal.className = 'modal';
    chatModal.innerHTML = `
        <div class="modal-content ai-chat-content">
            <span class="close" onclick="closeAIChat()">&times;</span>
            <h2>🤖 GitFlow AI Assistant</h2>
            <div class="chat-container">
                <div class="chat-messages" id="chatMessages">
                    <div class="chat-message ai">
                        <span class="ai-icon">🤖</span>
                        <span>Hello! I'm your AI Git assistant. Ask me anything about Git operations!</span>
                    </div>
                </div>
                <div class="chat-input-container">
                    <input type="text" id="chatInput" placeholder="Ask me about Git..." onkeypress="handleChatKeyPress(event)">
                    <button onclick="sendChatMessage()" class="btn-primary">Send</button>
                </div>
            </div>
            <div class="quick-actions">
                <h4>Quick Actions:</h4>
                <button onclick="askQuickQuestion('How do I commit my changes?')" class="quick-btn">Commit Changes</button>
                <button onclick="askQuickQuestion('How do I create a new branch?')" class="quick-btn">New Branch</button>
                <button onclick="askQuickQuestion('How do I undo my last commit?')" class="quick-btn">Undo Commit</button>
                <button onclick="getGitStatus()" class="quick-btn">Check Status</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(chatModal);
    chatModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Focus on input
    document.getElementById('chatInput').focus();
}

function closeAIChat() {
    const chatModal = document.getElementById('aiChatModal');
    if (chatModal) {
        chatModal.remove();
        document.body.style.overflow = 'auto';
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const query = input.value.trim();
    
    if (!query) return;
    
    // Add user message to chat
    addChatMessage(query, 'user');
    input.value = '';
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        // Send to AI backend
        const response = await fetch(`${API_BASE_URL}/api/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (data.success) {
            // Add AI response
            addAIResponse(data);
        } else {
            addChatMessage(`Sorry, I encountered an error: ${data.message}`, 'ai');
        }
        
    } catch (error) {
        removeTypingIndicator(typingId);
        addChatMessage('Sorry, I\'m having trouble connecting to the AI service. Please try again.', 'ai');
        console.error('Chat error:', error);
    }
}

function askQuickQuestion(question) {
    const input = document.getElementById('chatInput');
    input.value = question;
    sendChatMessage();
}

async function getGitStatus() {
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/status`);
        const data = await response.json();
        
        removeTypingIndicator(typingId);
        
        if (data.success) {
            const status = data.status;
            let statusMessage = `📊 Repository Status:\n`;
            statusMessage += `🌿 Branch: ${status.current_branch || 'unknown'}\n`;
            statusMessage += `📦 Staged files: ${status.staged_files || 0}\n`;
            statusMessage += `📝 Unstaged files: ${status.unstaged_files || 0}\n`;
            statusMessage += `✨ Status: ${status.is_clean ? 'Clean' : 'Has changes'}`;
            
            addChatMessage(statusMessage, 'ai');
        } else {
            addChatMessage(`Status check failed: ${data.message}`, 'ai');
        }
        
    } catch (error) {
        removeTypingIndicator(typingId);
        addChatMessage('Failed to get repository status.', 'ai');
        console.error('Status error:', error);
    }
}

function addChatMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    
    if (sender === 'ai') {
        messageDiv.innerHTML = `
            <span class="ai-icon">🤖</span>
            <span>${message.replace(/\n/g, '<br>')}</span>
        `;
    } else {
        messageDiv.innerHTML = `<span>${message}</span>`;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addAIResponse(data) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Add interpretation
    if (data.interpretation) {
        addChatMessage(data.interpretation, 'ai');
    }
    
    // Add commands
    if (data.commands && data.commands.length > 0) {
        let commandsMessage = '💡 Suggested Commands:\n\n';
        data.commands.forEach((cmd, index) => {
            const riskEmoji = { 'safe': '✅', 'moderate': '⚠️', 'destructive': '🚨' };
            commandsMessage += `${index + 1}. ${riskEmoji[cmd.risk] || '•'} ${cmd.command}\n`;
            commandsMessage += `   ${cmd.help || cmd.description}\n\n`;
        });
        
        addChatMessage(commandsMessage, 'ai');
    }
    
    // Add warnings
    if (data.warnings && data.warnings.length > 0) {
        const warningsMessage = '⚠️ Warnings:\n' + data.warnings.join('\n');
        addChatMessage(warningsMessage, 'ai');
    }
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    const typingId = 'typing-' + Date.now();
    typingDiv.id = typingId;
    typingDiv.className = 'chat-message ai typing';
    typingDiv.innerHTML = `
        <span class="ai-icon">🤖</span>
        <span class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </span>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return typingId;
}

function removeTypingIndicator(typingId) {
    const typingElement = document.getElementById(typingId);
    if (typingElement) {
        typingElement.remove();
    }
}

async function loadDemoConversations() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/demo`);
        const data = await response.json();
        
        if (data.success) {
            // Update demo modal with real conversations
            console.log('Demo conversations loaded:', data.conversations);
        }
    } catch (error) {
        console.error('Failed to load demo conversations:', error);
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('demoModal');
    if (event.target == modal) {
        closeDemo();
    }
}

// Add ripple effect CSS
const style = document.createElement('style');
style.textContent = `
    .btn-primary, .btn-secondary {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    /* Modal Styles */
    .modal {
        display: none;
        position: fixed;
        z-index: 2000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
    }
    
    .modal-content {
        background: linear-gradient(135deg, rgba(10, 10, 15, 0.95) 0%, rgba(20, 20, 30, 0.95) 100%);
        margin: 5% auto;
        padding: 2rem;
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        width: 90%;
        max-width: 600px;
        position: relative;
        color: white;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    }
    
    .close {
        color: rgba(255, 255, 255, 0.7);
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.3s ease;
    }
    
    .close:hover {
        color: #8b5cf6;
    }
    
    .demo-video {
        margin: 2rem 0;
    }
    
    .video-placeholder {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        border: 2px dashed rgba(139, 92, 246, 0.3);
    }
    
    .play-button {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.7;
    }
    
    .demo-features {
        background: rgba(139, 92, 246, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .demo-features h3 {
        margin-bottom: 1rem;
        color: #8b5cf6;
    }
    
    .demo-features ul {
        list-style: none;
        padding: 0;
    }
    
    .demo-features li {
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* AI Chat Styles */
    .ai-chat-content {
        max-width: 800px;
        height: 80vh;
        display: flex;
        flex-direction: column;
    }
    
    .chat-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        margin: 1rem 0;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        margin-bottom: 1rem;
        max-height: 400px;
    }
    
    .chat-message {
        margin-bottom: 1rem;
        padding: 0.75rem;
        border-radius: 12px;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .chat-message.user {
        background: rgba(139, 92, 246, 0.2);
        margin-left: 2rem;
        justify-content: flex-end;
    }
    
    .chat-message.ai {
        background: rgba(6, 182, 212, 0.2);
        margin-right: 2rem;
    }
    
    .chat-message.typing {
        background: rgba(6, 182, 212, 0.1);
    }
    
    .ai-icon {
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .typing-dots {
        display: flex;
        gap: 0.25rem;
    }
    
    .typing-dots span {
        width: 6px;
        height: 6px;
        background: #06b6d4;
        border-radius: 50%;
        animation: typing-bounce 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing-bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    .chat-input-container {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    .chat-input-container input {
        flex: 1;
        padding: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        background: rgba(0, 0, 0, 0.3);
        color: white;
        font-size: 0.9rem;
    }
    
    .chat-input-container input:focus {
        outline: none;
        border-color: #8b5cf6;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
    }
    
    .quick-actions {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .quick-actions h4 {
        margin-bottom: 0.5rem;
        color: #8b5cf6;
        font-size: 0.9rem;
    }
    
    .quick-btn {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #8b5cf6;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.25rem;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .quick-btn:hover {
        background: rgba(139, 92, 246, 0.2);
        border-color: rgba(139, 92, 246, 0.5);
    }
`;
document.head.appendChild(style);