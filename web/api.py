#!/usr/bin/env python3
"""
GitFlow AI Web API
Connects the frontend to the AI-powered Git conversation backend
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import json
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from gitflow_cli import SimpleGitAI
except ImportError:
    # Fallback if import fails
    class SimpleGitAI:
        def process_query(self, query):
            return {
                'interpretation': f"Processing: {query}",
                'commands': [{'command': 'git status', 'description': 'Check status', 'risk': 'safe'}],
                'warnings': []
            }
        
        def get_git_status(self):
            return {'current_branch': 'main', 'staged_files': 0, 'unstaged_files': 0, 'is_clean': True}

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)  # Enable CORS for all routes

# Initialize AI assistant
ai_assistant = SimpleGitAI()

@app.route('/')
def index():
    """Serve the main landing page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def api_ask():
    """Handle AI conversation requests"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Process query with AI
        response = ai_assistant.process_query(query)
        
        # Format response for frontend
        formatted_response = {
            'success': True,
            'query': query,
            'interpretation': response.get('interpretation', ''),
            'commands': response.get('commands', []),
            'warnings': response.get('warnings', []),
            'git_status': response.get('git_status', {}),
            'timestamp': get_timestamp()
        }
        
        return jsonify(formatted_response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to process query'
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get Git repository status"""
    try:
        git_status = ai_assistant.get_git_status()
        
        return jsonify({
            'success': True,
            'status': git_status,
            'timestamp': get_timestamp()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get repository status'
        }), 500

@app.route('/api/commit', methods=['POST'])
def api_commit():
    """Handle commit message generation"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        auto_stage = data.get('auto_stage', False)
        
        # Get current status
        git_status = ai_assistant.get_git_status()
        
        # Generate AI commit message if none provided
        if not message:
            # Simulate AI-generated commit message based on changes
            if git_status.get('staged_files', 0) > 0:
                message = "feat: implement new functionality\n\n- Add new features\n- Update existing code\n- Improve user experience"
            else:
                message = "No changes to commit"
        
        response = {
            'success': True,
            'message': message,
            'auto_stage': auto_stage,
            'git_status': git_status,
            'timestamp': get_timestamp()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate commit message'
        }), 500

@app.route('/api/demo', methods=['GET'])
def api_demo():
    """Get demo conversation examples"""
    demo_conversations = [
        {
            'query': 'How do I commit my changes?',
            'response': {
                'interpretation': 'I understand you want to commit your staged changes',
                'commands': [
                    {
                        'command': 'git commit -m "your message"',
                        'description': 'Commit your staged changes',
                        'risk': 'safe',
                        'help': 'This will create a new commit with your staged changes.'
                    }
                ],
                'warnings': []
            }
        },
        {
            'query': 'I want to undo my last commit but keep changes',
            'response': {
                'interpretation': 'I understand you want to undo the last commit while preserving your changes',
                'commands': [
                    {
                        'command': 'git reset --soft HEAD~1',
                        'description': 'Undo last commit but keep changes',
                        'risk': 'destructive',
                        'help': '⚠️ This removes the last commit but keeps your changes in the staging area.'
                    }
                ],
                'warnings': ['⚠️ This is a destructive operation!']
            }
        },
        {
            'query': 'How do I create a new branch?',
            'response': {
                'interpretation': 'I understand you want to create and switch to a new branch',
                'commands': [
                    {
                        'command': 'git checkout -b <branch-name>',
                        'description': 'Create and switch to a new branch',
                        'risk': 'safe',
                        'help': 'This creates a new branch and switches to it. Replace <branch-name> with your desired name.'
                    }
                ],
                'warnings': []
            }
        }
    ]
    
    return jsonify({
        'success': True,
        'conversations': demo_conversations,
        'timestamp': get_timestamp()
    })

@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'GitFlow AI API',
        'version': '1.0.0',
        'timestamp': get_timestamp()
    })

def get_timestamp():
    """Get current timestamp"""
    from datetime import datetime
    return datetime.now().isoformat()

if __name__ == '__main__':
    print("🚀 Starting GitFlow AI Web API...")
    print("📍 Frontend: http://localhost:5000")
    print("🔌 API: http://localhost:5000/api/")
    print("⏹️  Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)