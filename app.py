from flask import Flask, render_template, request, jsonify, session
import json
from story import story_data

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

@app.route('/')
def index():
    """Render the game interface."""
    # Initialize game state if not exists
    if 'game_state' not in session:
        session['game_state'] = {
            'current_node': 'start',
            'inventory': [],
            'visited': set(),
            'game_over': False
        }
    return render_template('index.html')

@app.route('/get_state', methods=['GET'])
def get_state():
    """Return the current game state as JSON."""
    if 'game_state' not in session:
        session['game_state'] = {
            'current_node': 'start',
            'inventory': [],
            'visited': set(),
            'game_over': False
        }
    return jsonify(session['game_state'])

@app.route('/get_node/<node_id>', methods=['GET'])
def get_node(node_id):
    """Return the story node data."""
    if node_id in story_data:
        return jsonify(story_data[node_id])
    return jsonify({'error': 'Node not found'}), 404

@app.route('/action', methods=['POST'])
def handle_action():
    """Handle player actions and update game state."""
    data = request.json
    action = data.get('action')
    target = data.get('target')
    game_state = session.get('game_state', {})
    
    if not game_state:
        return jsonify({'error': 'No game state'}), 400
    
    current_node_id = game_state.get('current_node', 'start')
    current_node = story_data.get(current_node_id)
    
    if not current_node:
        return jsonify({'error': 'Invalid node'}), 400
    
    # Handle game over state
    if game_state.get('game_over', False):
        if action == 'restart':
            session['game_state'] = {
                'current_node': 'start',
                'inventory': [],
                'visited': set(),
                'game_over': False
            }
            return jsonify({
                'success': True,
                'new_node': 'start',
                'message': 'Game restarted!'
            })
        return jsonify({'error': 'Game is over. Please restart.'}), 400
    
    # Process the action
    response = process_action(game_state, current_node, action, target)
    
    if response.get('error'):
        return jsonify(response), 400
    
    # Update session
    session['game_state'] = game_state
    session.modified = True
    
    return jsonify(response)

def process_action(game_state, current_node, action, target):
    """Process a player action and return the result."""
    # Check if action is valid
    if action not in current_node.get('actions', {}):
        return {'error': f'Invalid action: {action}'}
    
    action_data = current_node['actions'][action]
    
    # Check conditions
    if 'condition' in action_data:
        if not check_condition(game_state, action_data['condition']):
            return {'error': action_data.get('fail_message', 'You cannot do that.')}
    
    # Process effects
    if 'effects' in action_data:
        apply_effects(game_state, action_data['effects'])
    
    # Get the next node
    next_node = action_data.get('next', current_node.get('id'))
    
    # Check if next node exists
    if next_node not in story_data:
        return {'error': f'Error: Node {next_node} not found'}
    
    # Add to visited
    if 'visited' not in game_state:
        game_state['visited'] = set()
    game_state['visited'].add(next_node)
    
    # Update current node
    game_state['current_node'] = next_node
    
    # Check if game over
    if story_data[next_node].get('game_over', False):
        game_state['game_over'] = True
    
    return {
        'success': True,
        'new_node': next_node,
        'message': action_data.get('message', ''),
        'inventory': game_state.get('inventory', [])
    }

def check_condition(game_state, condition):
    """Check if a condition is met."""
    if 'has_item' in condition:
        return condition['has_item'] in game_state.get('inventory', [])
    elif 'visited' in condition:
        return condition['visited'] in game_state.get('visited', set())
    elif 'not_has_item' in condition:
        return condition['not_has_item'] not in game_state.get('inventory', [])
    return True

def apply_effects(game_state, effects):
    """Apply effects to the game state."""
    if 'add_item' in effects:
        if effects['add_item'] not in game_state.get('inventory', []):
            game_state.setdefault('inventory', []).append(effects['add_item'])
    if 'remove_item' in effects:
        inventory = game_state.get('inventory', [])
        if effects['remove_item'] in inventory:
            inventory.remove(effects['remove_item'])
    if 'set_flag' in effects:
        game_state[effects['set_flag']] = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
