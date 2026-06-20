// Game state
let gameState = {
    current_node: 'start',
    inventory: [],
    visited: [],
    game_over: false
};

// DOM elements
const storyText = document.getElementById('story-text');
const nodeTitle = document.getElementById('node-title');
const actionButtons = document.getElementById('action-buttons');
const inventoryList = document.getElementById('inventory-list');
const messageDiv = document.getElementById('message');

// Initialize game
document.addEventListener('DOMContentLoaded', () => {
    loadGameState();
    loadNode(gameState.current_node);
});

// Load game state from server
async function loadGameState() {
    try {
        const response = await fetch('/get_state');
        gameState = await response.json();
        gameState.visited = gameState.visited || [];
        updateInventory();
    } catch (error) {
        console.error('Error loading game state:', error);
        showMessage('Error loading game state. Please refresh.', 'error');
    }
}

// Load a story node
async function loadNode(nodeId) {
    try {
        const response = await fetch(`/get_node/${nodeId}`);
        if (!response.ok) {
            throw new Error('Node not found');
        }
        const node = await response.json();
        displayNode(node);
        renderActions(node);
        updateInventory();
    } catch (error) {
        console.error('Error loading node:', error);
        showMessage('Error loading story. Please refresh.', 'error');
        actionButtons.innerHTML = '';
        storyText.textContent = 'An error occurred. Please refresh the page.';
    }
}

// Display the node content
function displayNode(node) {
    // Update title
    nodeTitle.textContent = node.title || 'Untitled';
    
    // Update text
    storyText.textContent = node.text || 'No description available.';
    
    // Scroll to top of story
    document.getElementById('story-display').scrollTop = 0;
    
    // Hide any previous message
    hideMessage();
}

// Render action buttons
function renderActions(node) {
    const actions = node.actions || {};
    const actionKeys = Object.keys(actions);
    
    if (actionKeys.length === 0) {
        actionButtons.innerHTML = '<p style="color: #666; font-style: italic;">No actions available.</p>';
        return;
    }
    
    actionButtons.innerHTML = '';
    
    // Check if game is over
    const isGameOver = gameState.game_over || node.game_over || false;
    
    actionKeys.forEach(actionKey => {
        const action = actions[actionKey];
        const button = document.createElement('button');
        button.className = 'action-btn';
        
        // Format action label
        const label = actionKey
            .replace(/_/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
        
        button.textContent = label;
        
        // Special handling for restart
        if (actionKey === 'restart') {
            button.classList.add('restart-btn');
            button.addEventListener('click', () => handleAction(actionKey, action));
        } else {
            button.addEventListener('click', () => handleAction(actionKey, action));
        }
        
        // Disable button if game is over (except restart)
        if (isGameOver && actionKey !== 'restart') {
            button.disabled = true;
            button.title = 'Game is over. Please restart.';
        }
        
        actionButtons.appendChild(button);
    });
}

// Handle action
async function handleAction(actionKey, actionData) {
    // Disable all buttons during request
    const buttons = document.querySelectorAll('.action-btn');
    buttons.forEach(btn => btn.disabled = true);
    
    try {
        const response = await fetch('/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: actionKey,
                target: actionData.next || gameState.current_node
            })
        });
        
        const result = await response.json();
        
        if (result.error) {
            showMessage(result.error, 'error');
            // Re-enable buttons
            buttons.forEach(btn => btn.disabled = false);
            return;
        }
        
        // Check if we're restarting
        if (actionKey === 'restart') {
            // Reload the page to reset everything
            window.location.reload();
            return;
        }
        
        // Show success message
        if (result.message) {
            showMessage(result.message, 'success');
        }
        
        // Update game state
        gameState.current_node = result.new_node;
        gameState.inventory = result.inventory || gameState.inventory || [];
        
        // Update inventory display
        updateInventory();
        
        // Load the new node
        await loadNode(result.new_node);
        
    } catch (error) {
        console.error('Error handling action:', error);
        showMessage('An error occurred. Please try again.', 'error');
    } finally {
        // Re-enable buttons
        buttons.forEach(btn => btn.disabled = false);
    }
}

// Update inventory display
function updateInventory() {
    const inventory = gameState.inventory || [];
    if (inventory.length === 0) {
        inventoryList.textContent = 'Empty';
    } else {
        inventoryList.textContent = inventory.map(item => 
            item.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
        ).join(', ');
    }
}

// Show message
function showMessage(text, type = 'info') {
    messageDiv.textContent = text;
    messageDiv.className = type || '';
    messageDiv.classList.remove('hidden');
}

// Hide message
function hideMessage() {
    messageDiv.classList.add('hidden');
    messageDiv.className = '';
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Press 'R' to restart when game is over
    if (e.key === 'r' && gameState.game_over) {
        const restartBtn = document.querySelector('.restart-btn');
        if (restartBtn && !restartBtn.disabled) {
            restartBtn.click();
        }
    }
    
    // Press number keys for actions
    if (e.key >= '1' && e.key <= '9') {
        const index = parseInt(e.key) - 1;
        const buttons = document.querySelectorAll('.action-btn:not(:disabled)');
        if (buttons[index]) {
            buttons[index].click();
        }
    }
});

console.log('🎮 Text Adventure Game loaded!');
console.log('📖 Type your actions or click the buttons.');
console.log('⌨️ Use number keys (1-9) for quick actions.');
