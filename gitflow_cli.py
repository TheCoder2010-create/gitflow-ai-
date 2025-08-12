#!/usr/bin/env python3
"""
GitFlow AI - Simple CLI Implementation
AI-Powered Git Conversations (Working Version)
"""

import click
import sys
import os
import re
import subprocess
from typing import List, Dict, Optional

# Simple AI conversation system without complex imports
class SimpleGitAI:
    """Simple AI-powered Git assistant"""
    
    def __init__(self):
        self.git_patterns = {
            # Commit operations
            r'commit|save changes|record changes': {
                'command': 'git commit',
                'description': 'Commit your staged changes',
                'risk': 'safe',
                'help': 'This will create a new commit with your staged changes. Make sure to stage files first with "git add".'
            },
            r'undo.*commit|revert.*commit': {
                'command': 'git revert HEAD',
                'description': 'Revert the last commit',
                'risk': 'moderate',
                'help': 'This creates a new commit that undoes the changes from the last commit.'
            },
            r'reset.*commit|undo.*last.*commit': {
                'command': 'git reset --soft HEAD~1',
                'description': 'Undo last commit but keep changes',
                'risk': 'destructive',
                'help': '⚠️ This removes the last commit but keeps your changes in the staging area.'
            },
            
            # Branch operations
            r'create.*branch|new.*branch': {
                'command': 'git checkout -b <branch-name>',
                'description': 'Create and switch to a new branch',
                'risk': 'safe',
                'help': 'This creates a new branch and switches to it. Replace <branch-name> with your desired name.'
            },
            r'switch.*branch|change.*branch': {
                'command': 'git checkout <branch-name>',
                'description': 'Switch to an existing branch',
                'risk': 'safe',
                'help': 'This switches to an existing branch. Replace <branch-name> with the target branch.'
            },
            r'merge.*branch': {
                'command': 'git merge <branch-name>',
                'description': 'Merge a branch into current branch',
                'risk': 'moderate',
                'help': 'This merges another branch into your current branch. Make sure you\'re on the target branch first.'
            },
            r'delete.*branch|remove.*branch': {
                'command': 'git branch -d <branch-name>',
                'description': 'Delete a branch',
                'risk': 'destructive',
                'help': '⚠️ This permanently deletes a branch. Make sure it\'s merged first.'
            },
            
            # Status and info
            r'status|what.*changed|current.*state': {
                'command': 'git status',
                'description': 'Show repository status',
                'risk': 'safe',
                'help': 'This shows the current state of your working directory and staging area.'
            },
            r'log|history|commits': {
                'command': 'git log --oneline -10',
                'description': 'Show recent commit history',
                'risk': 'safe',
                'help': 'This shows the last 10 commits in a compact format.'
            },
            r'diff|changes|what.*different': {
                'command': 'git diff',
                'description': 'Show changes in working directory',
                'risk': 'safe',
                'help': 'This shows the differences between your working directory and the last commit.'
            },
            
            # Staging operations
            r'add.*files|stage.*files': {
                'command': 'git add .',
                'description': 'Stage all changes',
                'risk': 'safe',
                'help': 'This stages all modified and new files for the next commit.'
            },
            r'unstage|remove.*staged': {
                'command': 'git reset HEAD',
                'description': 'Unstage all files',
                'risk': 'moderate',
                'help': 'This removes files from the staging area but keeps your changes.'
            },
            
            # Remote operations
            r'push|upload|send': {
                'command': 'git push',
                'description': 'Push commits to remote repository',
                'risk': 'moderate',
                'help': 'This uploads your commits to the remote repository.'
            },
            r'pull|download|fetch': {
                'command': 'git pull',
                'description': 'Pull changes from remote repository',
                'risk': 'moderate',
                'help': 'This downloads and merges changes from the remote repository.'
            },
            
            # Stash operations
            r'stash|save.*work|temporary.*save': {
                'command': 'git stash',
                'description': 'Temporarily save changes',
                'risk': 'safe',
                'help': 'This temporarily saves your uncommitted changes so you can switch branches.'
            }
        }
    
    def get_git_status(self) -> Dict:
        """Get current Git repository status"""
        try:
            # Check if we're in a Git repository
            result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                return {'error': 'Not a Git repository'}
            
            # Get current branch
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True)
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
            
            # Get status
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True)
            status_lines = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            
            staged_files = [line for line in status_lines if line.startswith(('A ', 'M ', 'D '))]
            unstaged_files = [line for line in status_lines if line.startswith((' M', ' D', '??'))]
            
            return {
                'current_branch': current_branch,
                'staged_files': len(staged_files),
                'unstaged_files': len(unstaged_files),
                'is_clean': len(status_lines) == 0
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def process_query(self, query: str) -> Dict:
        """Process natural language Git query"""
        query_lower = query.lower()
        
        # Find matching patterns
        matches = []
        for pattern, info in self.git_patterns.items():
            if re.search(pattern, query_lower):
                matches.append(info)
        
        if not matches:
            return {
                'interpretation': "I understand you're asking about Git, but I couldn't identify a specific command.",
                'suggestion': "Try asking about: commit, branch, status, merge, push, pull, or stash operations.",
                'commands': []
            }
        
        # Get repository status for context
        git_status = self.get_git_status()
        
        # Build response
        response = {
            'interpretation': f"I understand you want to: {matches[0]['description']}",
            'commands': matches,
            'git_status': git_status,
            'warnings': []
        }
        
        # Add contextual warnings
        if not git_status.get('error'):
            for match in matches:
                if match['risk'] == 'destructive':
                    response['warnings'].append(f"⚠️ {match['command']} is a destructive operation!")
                
                # Context-specific warnings
                if 'checkout' in match['command'] and git_status.get('unstaged_files', 0) > 0:
                    response['warnings'].append("⚠️ You have unstaged changes. Consider stashing them first.")
        
        return response

# Initialize AI assistant
ai_assistant = SimpleGitAI()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """🤖 GitFlow AI - Intelligent Git Workflow Assistant
    
    Transform your Git experience with AI-powered assistance.
    Ask questions in natural language and get intelligent suggestions.
    """
    pass

@cli.command()
@click.argument('query', required=False)
@click.option('--interactive', '-i', is_flag=True, help='Start interactive conversation mode')
def ask(query, interactive):
    """Ask the AI assistant about Git operations
    
    Examples:
      gitflow ask "How do I commit my changes?"
      gitflow ask "I want to undo my last commit"
      gitflow ask --interactive
    """
    
    if interactive:
        click.echo("🤖 GitFlow AI Interactive Mode")
        click.echo("Type 'exit' or 'quit' to end the conversation")
        click.echo("-" * 50)
        
        while True:
            try:
                user_input = click.prompt("\n❓ You", type=str)
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    click.echo("👋 Goodbye! Happy coding!")
                    break
                
                process_single_query(user_input)
                
            except (KeyboardInterrupt, EOFError):
                click.echo("\n👋 Goodbye! Happy coding!")
                break
    else:
        if not query:
            query = click.prompt("What would you like to do with Git?")
        
        process_single_query(query)

def process_single_query(query: str):
    """Process a single query and display results"""
    click.echo(f"\n🤖 Processing: {query}")
    
    # Get AI response
    response = ai_assistant.process_query(query)
    
    # Display interpretation
    click.echo(f"\n💭 {response['interpretation']}")
    
    # Display suggested commands
    if response['commands']:
        click.echo("\n💡 Suggested Git Commands:")
        for i, cmd in enumerate(response['commands'], 1):
            risk_emoji = {'safe': '✅', 'moderate': '⚠️', 'destructive': '🚨'}
            click.echo(f"   {i}. {risk_emoji[cmd['risk']]} {cmd['command']}")
            click.echo(f"      📝 {cmd['help']}")
    
    # Display warnings
    if response['warnings']:
        click.echo("\n⚠️ Important Warnings:")
        for warning in response['warnings']:
            click.echo(f"   • {warning}")
    
    # Display Git status
    git_status = response.get('git_status', {})
    if not git_status.get('error'):
        click.echo(f"\n📊 Repository Status:")
        click.echo(f"   🌿 Current branch: {git_status.get('current_branch', 'unknown')}")
        click.echo(f"   📦 Staged files: {git_status.get('staged_files', 0)}")
        click.echo(f"   📝 Unstaged files: {git_status.get('unstaged_files', 0)}")
        click.echo(f"   ✨ Repository: {'Clean' if git_status.get('is_clean') else 'Has changes'}")

@cli.command()
def status():
    """Show enhanced Git status with AI insights"""
    click.echo("📊 GitFlow AI Repository Status")
    click.echo("=" * 40)
    
    git_status = ai_assistant.get_git_status()
    
    if git_status.get('error'):
        click.echo(f"❌ {git_status['error']}")
        return
    
    # Display status
    click.echo(f"🌿 Current branch: {git_status.get('current_branch', 'unknown')}")
    click.echo(f"📦 Staged files: {git_status.get('staged_files', 0)}")
    click.echo(f"📝 Unstaged files: {git_status.get('unstaged_files', 0)}")
    click.echo(f"✨ Repository: {'Clean' if git_status.get('is_clean') else 'Has changes'}")
    
    # AI insights
    click.echo("\n🤖 AI Insights:")
    if git_status.get('is_clean'):
        click.echo("   ✨ Repository is clean and up to date!")
    elif git_status.get('staged_files', 0) > 0:
        click.echo("   💡 You have staged changes ready to commit")
        click.echo("   💬 Try: gitflow ask 'how do I commit my changes?'")
    elif git_status.get('unstaged_files', 0) > 0:
        click.echo("   📝 You have unstaged changes")
        click.echo("   💬 Try: gitflow ask 'how do I stage my files?'")

@cli.command()
def demo():
    """Run interactive demo of GitFlow AI features"""
    click.echo("🎬 GitFlow AI Interactive Demo")
    click.echo("=" * 40)
    
    demo_queries = [
        "How do I check the status of my repository?",
        "I want to commit my changes",
        "How do I create a new branch?",
        "I made a mistake in my last commit, how do I fix it?",
        "How do I merge my feature branch safely?"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        click.echo(f"\n🎯 Demo {i}/5: {query}")
        if click.confirm("Run this demo?", default=True):
            process_single_query(query)
        click.echo("-" * 40)
    
    click.echo("\n✨ Demo completed! Try 'gitflow ask --interactive' for more.")

@cli.command()
def init():
    """Initialize GitFlow AI in current repository"""
    click.echo("🚀 Initializing GitFlow AI...")
    
    git_status = ai_assistant.get_git_status()
    
    if git_status.get('error'):
        click.echo(f"❌ {git_status['error']}")
        click.echo("Please run this command in a Git repository.")
        return
    
    click.echo("✅ GitFlow AI initialized successfully!")
    click.echo(f"📍 Current branch: {git_status.get('current_branch', 'unknown')}")
    click.echo("\n🎯 You can now use:")
    click.echo("   • gitflow ask 'your question'")
    click.echo("   • gitflow status")
    click.echo("   • gitflow ask --interactive")
    click.echo("   • gitflow demo")

if __name__ == '__main__':
    cli()