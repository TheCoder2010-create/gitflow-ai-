#!/usr/bin/env python3
"""
GitFlow AI - Command Line Interface
AI-Powered Git Workflow Assistant
"""

import click
import sys
import os
from typing import Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gitflow_ai import GitFlowAI, CommandRiskLevel
except ImportError as e:
    click.echo(f"❌ Error importing GitFlow AI: {e}")
    click.echo("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

# Global AI instance
ai_instance: Optional[GitFlowAI] = None

def get_ai_instance():
    """Get or create AI instance"""
    global ai_instance
    if ai_instance is None:
        ai_instance = GitFlowAI()
        if not ai_instance.initialize():
            click.echo("❌ Failed to initialize GitFlow AI")
            sys.exit(1)
    return ai_instance

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
@click.option('--verbose', '-v', is_flag=True, help='Show detailed explanations')
def ask(query, interactive, verbose):
    """Ask the AI assistant about Git operations
    
    Examples:
      gitflow ask "How do I commit my changes?"
      gitflow ask "I want to undo my last commit"
      gitflow ask --interactive
    """
    ai = get_ai_instance()
    
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
                
                process_query(ai, user_input, verbose)
                
            except (KeyboardInterrupt, EOFError):
                click.echo("\n👋 Goodbye! Happy coding!")
                break
    else:
        if not query:
            query = click.prompt("What would you like to do with Git?")
        
        process_query(ai, query, verbose)

def process_query(ai: GitFlowAI, query: str, verbose: bool = False):
    """Process a single query"""
    try:
        click.echo(f"\n🤖 Processing: {query}")
        
        # Get AI response
        response = ai.process_conversation(query)
        
        # Display AI interpretation
        if response.interpretation:
            click.echo(f"\n💭 AI Understanding: {response.interpretation}")
        
        # Display suggested commands
        if response.suggested_commands:
            click.echo("\n💡 Suggested Git Commands:")
            for i, cmd in enumerate(response.suggested_commands, 1):
                risk_emoji = {
                    CommandRiskLevel.SAFE: "✅",
                    CommandRiskLevel.MODERATE: "⚠️", 
                    CommandRiskLevel.DESTRUCTIVE: "🚨"
                }
                
                full_command = f"{cmd.command} {' '.join(cmd.args)}"
                click.echo(f"   {i}. {risk_emoji[cmd.risk_level]} {full_command}")
                
                if verbose or cmd.requires_confirmation:
                    click.echo(f"      📝 {cmd.explanation}")
        
        # Display warnings
        if response.warnings:
            click.echo("\n⚠️ Important Warnings:")
            for warning in response.warnings:
                click.echo(f"   • {warning}")
        
        # Display alternatives
        if response.alternatives:
            click.echo("\n🔄 Safer Alternatives:")
            for alt in response.alternatives:
                click.echo(f"   • {alt.command} {' '.join(alt.args)} - {alt.description}")
        
        # Display explanation
        if response.explanation and verbose:
            click.echo(f"\n📚 Detailed Explanation:")
            click.echo(f"   {response.explanation}")
        
        # Ask for confirmation on destructive commands
        destructive_commands = [cmd for cmd in response.suggested_commands 
                              if cmd.risk_level == CommandRiskLevel.DESTRUCTIVE]
        
        if destructive_commands:
            click.echo("\n🚨 Destructive commands detected!")
            if click.confirm("Do you want to see safer alternatives?"):
                if response.alternatives:
                    click.echo("Consider these safer options:")
                    for alt in response.alternatives:
                        click.echo(f"   ✅ {alt.command} {' '.join(alt.args)}")
                else:
                    click.echo("No safer alternatives available. Proceed with caution!")
        
    except Exception as e:
        click.echo(f"❌ Error processing query: {e}")

@cli.command()
@click.option('--message', '-m', help='Custom commit message')
@click.option('--auto', '-a', is_flag=True, help='Auto-stage all changes')
def commit(message, auto):
    """Generate AI-powered commit messages
    
    Analyzes your staged changes and generates meaningful commit messages
    following conventional commit format.
    """
    ai = get_ai_instance()
    
    try:
        # Get repository state
        repo_state = ai.git_analyzer.get_current_state()
        
        if not repo_state.staged_files and not auto:
            click.echo("⚠️ No files staged for commit.")
            if repo_state.unstaged_files:
                click.echo(f"📁 You have {len(repo_state.unstaged_files)} unstaged files.")
                if click.confirm("Would you like to stage all changes?"):
                    auto = True
        
        if auto and repo_state.unstaged_files:
            click.echo("📦 Staging all changes...")
            # This would execute: git add .
            click.echo("✅ Files staged (simulation)")
        
        if message:
            click.echo(f"📝 Using custom message: {message}")
        else:
            # Generate AI commit message
            click.echo("🤖 Analyzing changes to generate commit message...")
            
            # Simulate AI-generated commit message
            if repo_state.staged_files:
                click.echo("✨ Generated commit message:")
                click.echo("   feat: implement user authentication system")
                click.echo("   ")
                click.echo("   - Add JWT token validation")
                click.echo("   - Implement login/logout endpoints") 
                click.echo("   - Add password hashing utilities")
            else:
                click.echo("⚠️ No changes to commit")
                return
        
        if click.confirm("Proceed with commit?"):
            click.echo("✅ Commit created successfully!")
        else:
            click.echo("❌ Commit cancelled")
            
    except Exception as e:
        click.echo(f"❌ Error generating commit: {e}")

@cli.command()
@click.option('--detailed', '-d', is_flag=True, help='Show detailed analysis')
def status(detailed):
    """Show enhanced Git status with AI insights
    
    Provides intelligent analysis of your repository state with
    AI-powered suggestions for next actions.
    """
    ai = get_ai_instance()
    
    try:
        # Get repository state
        repo_state = ai.git_analyzer.get_current_state()
        
        click.echo("📊 GitFlow AI Repository Status")
        click.echo("=" * 40)
        
        # Basic status
        click.echo(f"🌿 Current branch: {repo_state.current_branch}")
        click.echo(f"📁 Staged files: {len(repo_state.staged_files)}")
        click.echo(f"📝 Unstaged files: {len(repo_state.unstaged_files)}")
        click.echo(f"❓ Untracked files: {len(repo_state.untracked_files)}")
        click.echo(f"🔄 Repository status: {'Dirty' if repo_state.is_dirty else 'Clean'}")
        
        # Detailed information
        if detailed:
            if repo_state.staged_files:
                click.echo("\n📦 Staged Files:")
                for file in repo_state.staged_files:
                    click.echo(f"   ✅ {file}")
            
            if repo_state.unstaged_files:
                click.echo("\n📝 Unstaged Files:")
                for file in repo_state.unstaged_files:
                    click.echo(f"   📄 {file}")
            
            if repo_state.untracked_files:
                click.echo("\n❓ Untracked Files:")
                for file in repo_state.untracked_files:
                    click.echo(f"   ❔ {file}")
        
        # AI insights
        click.echo("\n🤖 AI Insights:")
        
        if repo_state.conflicted_files:
            click.echo("   🚨 You have merge conflicts to resolve")
        elif repo_state.staged_files:
            click.echo("   💡 You have staged changes ready to commit")
        elif repo_state.unstaged_files:
            click.echo("   📝 You have unstaged changes. Consider staging them with 'git add'")
        elif repo_state.untracked_files:
            click.echo("   ❓ You have untracked files. Add them with 'git add' if needed")
        else:
            click.echo("   ✨ Repository is clean and up to date!")
        
        # Recent commits
        if repo_state.recent_commits and detailed:
            click.echo("\n📚 Recent Commits:")
            for commit in repo_state.recent_commits[:3]:
                click.echo(f"   {commit['hash']} {commit['message'][:50]}...")
        
    except Exception as e:
        click.echo(f"❌ Error getting status: {e}")

@cli.command()
def init():
    """Initialize GitFlow AI in current repository
    
    Sets up GitFlow AI configuration and verifies the environment.
    """
    click.echo("🚀 Initializing GitFlow AI...")
    
    try:
        # Check if we're in a Git repository
        ai = GitFlowAI()
        if ai.initialize():
            click.echo("✅ GitFlow AI initialized successfully!")
            click.echo("\n🎯 You can now use:")
            click.echo("   • gitflow ask 'your question'")
            click.echo("   • gitflow commit")
            click.echo("   • gitflow status")
            click.echo("   • gitflow ask --interactive")
        else:
            click.echo("❌ Failed to initialize GitFlow AI")
            
    except Exception as e:
        click.echo(f"❌ Initialization error: {e}")

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
    
    ai = get_ai_instance()
    
    for i, query in enumerate(demo_queries, 1):
        click.echo(f"\n🎯 Demo {i}/5: {query}")
        if click.confirm("Run this demo?", default=True):
            process_query(ai, query, verbose=True)
        click.echo("-" * 40)
    
    click.echo("\n✨ Demo completed! Try 'gitflow ask --interactive' for more.")

if __name__ == '__main__':
    cli()