let aiConversationHistory = [];
let aiIsProcessing = false;

function toggleAIChat() {
    const panel = document.getElementById('aiChatPanel');
    const fab = document.getElementById('aiFab');
    panel.classList.toggle('open');
    fab.classList.toggle('active');
    if (panel.classList.contains('open')) {
        document.getElementById('aiChatInput').focus();
        scrollToBottom();
    }
}

function autoResizeInput(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    const btn = document.getElementById('aiSendBtn');
    btn.disabled = !textarea.value.trim();
}

function handleInputKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function addMessage(role, content, isTyping) {
    const container = document.getElementById('aiChatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `ai-message ai-message-${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'ai-message-avatar';
    avatar.innerHTML = role === 'user'
        ? '<i class="fas fa-user"></i>'
        : '<i class="fas fa-robot"></i>';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'ai-message-content';

    if (isTyping) {
        contentDiv.innerHTML = '<div class="ai-typing"><span></span><span></span><span></span></div>';
        msgDiv.id = 'aiTypingIndicator';
    } else {
        contentDiv.innerHTML = '<p>' + escapeHtml(content) + '</p>';
    }

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(contentDiv);
    container.appendChild(msgDiv);
    scrollToBottom();
}

function updateTypingToContent(content) {
    const typing = document.getElementById('aiTypingIndicator');
    if (typing) {
        const contentDiv = typing.querySelector('.ai-message-content');
        if (contentDiv) {
            contentDiv.innerHTML = '<p>' + formatAIResponse(content) + '</p>';
        }
        typing.id = '';
    }
}

function formatAIResponse(text) {
    const escaped = escapeHtml(text);
    const withBold = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    const withLineBreaks = withBold.replace(/\n/g, '<br>');
    return withLineBreaks;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    const container = document.getElementById('aiChatMessages');
    requestAnimationFrame(() => {
        container.scrollTop = container.scrollHeight;
    });
}

async function sendMessage() {
    if (aiIsProcessing) return;

    const input = document.getElementById('aiChatInput');
    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    autoResizeInput(input);
    addMessage('user', message, false);
    aiConversationHistory.push({ role: 'user', content: message });

    addMessage('system', '', true);
    aiIsProcessing = true;
    document.getElementById('aiSendBtn').disabled = true;

    try {
        const pageContext = buildPageContext();
        const resp = await fetch('/ai/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                dataset_id: pageContext.dataset_id || null,
                history: aiConversationHistory.slice(-20),
                page_context: pageContext
            })
        });

        const data = await resp.json();
        if (data.error) {
            updateTypingToContent('Error: ' + data.error);
        } else {
            updateTypingToContent(data.response);
            aiConversationHistory.push({ role: 'assistant', content: data.response });
        }
    } catch (err) {
        updateTypingToContent('Error: Could not connect to the AI service. Please try again.');
    } finally {
        aiIsProcessing = false;
        document.getElementById('aiSendBtn').disabled = false;
        scrollToBottom();
    }
}

function buildPageContext() {
    const ctx = {
        page: '',
        dataset_id: null
    };

    const path = window.location.pathname;
    ctx.page = path;

    const match = path.match(/\/(\d+)/);
    if (match) {
        ctx.dataset_id = parseInt(match[1], 10);
    }

    if (path.includes('validation')) ctx.workflow_step = 'validation';
    else if (path.includes('eda')) ctx.workflow_step = 'eda';
    else if (path.includes('preprocessing')) ctx.workflow_step = 'preprocessing';
    else if (path.includes('forecasting') || path.includes('forecast')) ctx.workflow_step = 'forecasting';
    else if (path.includes('compare')) ctx.workflow_step = 'comparison';
    else if (path.includes('reports') || path.includes('report')) ctx.workflow_step = 'reports';
    else if (path.includes('dashboard')) ctx.workflow_step = 'dashboard';
    else if (path.includes('upload')) ctx.workflow_step = 'upload';

    return ctx;
}

function clearConversation() {
    aiConversationHistory = [];
    const container = document.getElementById('aiChatMessages');
    container.innerHTML = '';
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'ai-message ai-message-system';
    welcomeDiv.innerHTML = `
        <div class="ai-message-avatar"><i class="fas fa-robot"></i></div>
        <div class="ai-message-content">
            <p>Hello! I'm your ForecastIQ AI Copilot. I can help you understand your datasets, forecasting results, and workflow. How can I assist you today?</p>
        </div>`;
    container.appendChild(welcomeDiv);
}

document.addEventListener('DOMContentLoaded', function() {
    const chatPanel = document.getElementById('aiChatPanel');
    if (chatPanel) {
        chatPanel.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    document.addEventListener('click', function(e) {
        const panel = document.getElementById('aiChatPanel');
        const fab = document.getElementById('aiFab');
        if (panel && panel.classList.contains('open')) {
            if (!panel.contains(e.target) && !fab.contains(e.target)) {
                toggleAIChat();
            }
        }
    });
});
