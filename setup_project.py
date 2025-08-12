#!/usr/bin/env python3
"""
Setup script for Intelligent Git Workflow Assistant
This script sets up the basic project structure and dependencies
"""

import os
import subprocess
import sys

def create_project_structure():
    """Create the basic project directory structure"""
    directories = [
        "src",
        "src/models",
        "src/services", 
        "src/utils",
        "tests",
        "models",  # For storing downloaded models
        "config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_basic_files():
    """Create basic project files"""
    
    # Create requirements.txt
    requirements = """torch>=2.0.0
transformers>=4.30.0
accelerate>=0.20.0
datasets>=2.0.0
gitpython>=3.1.0
click>=8.0.0
pyyaml>=6.0
colorama>=0.4.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✅ Created requirements.txt")
    
    # Create basic config file
    config = """# Intelligent Git Workflow Assistant Configuration

model:
  name: "microsoft/DialoGPT-small"  # Small model for testing
  cache_dir: "./models"
  max_length: 512
  temperature: 0.7

git:
  default_branch: "main"
  conventional_commits: true
  
assistant:
  max_context_length: 2048
  response_timeout: 30
"""
    
    with open("config/config.yaml", "w") as f:
        f.write(config)
    print("✅ Created config/config.yaml")
    
    # Create basic CLI entry point
    cli_code = '''#!/usr/bin/env python3
"""
Command Line Interface for Intelligent Git Workflow Assistant
"""

import click
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

@click.group()
def cli():
    """Intelligent Git Workflow Assistant - AI-powered Git helper"""
    pass

@cli.command()
@click.argument('query', required=False)
def ask(query):
    """Ask the AI assistant about Git operations"""
    if not query:
        query = click.prompt("What would you like to do with Git?")
    
    click.echo(f"🤖 Processing: {query}")
    click.echo("🚧 AI processing not yet implemented - coming soon!")

@cli.command()
def commit():
    """Generate AI-powered commit messages"""
    click.echo("🤖 Analyzing your changes...")
    click.echo("🚧 AI commit message generation not yet implemented - coming soon!")

@cli.command()
def status():
    """Show enhanced Git status with AI insights"""
    click.echo("📊 Git Status with AI Insights:")
    click.echo("🚧 AI status analysis not yet implemented - coming soon!")

if __name__ == '__main__':
    cli()
'''
    
    with open("git_assistant.py", "w") as f:
        f.write(cli_code)
    print("✅ Created git_assistant.py (CLI entry point)")

def main():
    """Main setup function"""
    print("🚀 Setting up Intelligent Git Workflow Assistant...")
    
    create_project_structure()
    create_basic_files()
    
    print("\n✅ Project setup complete!")
    print("\nNext steps:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Test the CLI: python git_assistant.py --help")
    print("3. Start implementing tasks from your spec!")
    print("\n🎯 Ready for your hackathon! Good luck!")

if __name__ == "__main__":
    main()