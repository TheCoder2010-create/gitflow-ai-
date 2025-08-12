#!/usr/bin/env python3
"""
Upload GitFlow AI to GitHub Repository
Automated script to initialize Git and push to GitHub
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def setup_git_repository():
    """Initialize Git repository and upload to GitHub"""
    print("🚀 GitFlow AI - GitHub Upload Script")
    print("=" * 50)
    
    # Check if we're already in a Git repository
    if os.path.exists('.git'):
        print("📁 Git repository already exists")
    else:
        # Initialize Git repository
        if not run_command("git init", "Initializing Git repository"):
            return False
    
    # Configure Git user (if not already configured)
    print("\n🔧 Configuring Git user...")
    run_command('git config user.name "Manav Sutar"', "Setting Git username")
    run_command('git config user.email "sutarmanav557@gmail.com"', "Setting Git email")
    
    # Add all files
    if not run_command("git add .", "Adding all files to Git"):
        return False
    
    # Create initial commit
    commit_message = "🚀 Initial commit: GitFlow AI - Intelligent Git Workflow Assistant\n\n✨ Features:\n- AI-Powered Git Conversations\n- Natural Language Interface\n- Smart Command Suggestions\n- Safety Validations\n- Web Interface\n- CLI Tool\n\nBuilt for OpenAI Hackathon 🏆"
    
    if not run_command(f'git commit -m "{commit_message}"', "Creating initial commit"):
        return False
    
    # Add GitHub remote
    github_url = "https://github.com/TheCoder2010-create/gitflow-ai-.git"
    if not run_command(f"git remote add origin {github_url}", "Adding GitHub remote"):
        # Remote might already exist, try to set URL
        run_command(f"git remote set-url origin {github_url}", "Setting GitHub remote URL")
    
    # Create main branch and push
    run_command("git branch -M main", "Setting main branch")
    
    print("\n🌐 Ready to push to GitHub!")
    print("📍 Repository: https://github.com/TheCoder2010-create/gitflow-ai")
    print("\n⚠️  IMPORTANT: You'll need to authenticate with GitHub")
    print("   Option 1: Use GitHub CLI (gh auth login)")
    print("   Option 2: Use Personal Access Token")
    print("   Option 3: Use SSH key")
    
    # Ask user if they want to push now
    response = input("\n❓ Do you want to push to GitHub now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Pushing to GitHub...")
        if run_command("git push -u origin main", "Pushing to GitHub"):
            print("\n🎉 SUCCESS! GitFlow AI uploaded to GitHub!")
            print(f"🔗 Repository URL: {github_url}")
            print("\n📋 Next steps:")
            print("1. ✅ Repository created and uploaded")
            print("2. 🌐 Set up GitHub Pages (optional)")
            print("3. 🚀 Deploy to Vercel/Netlify (optional)")
            print("4. 📝 Update repository description on GitHub")
            print("5. 🏷️  Add topics: ai, git, assistant, openai, hackathon")
            return True
        else:
            print("\n❌ Push failed. Please check your GitHub authentication.")
            print("\n🔧 Troubleshooting:")
            print("1. Make sure the repository exists on GitHub")
            print("2. Check your GitHub authentication")
            print("3. Try: gh auth login (if using GitHub CLI)")
            print("4. Or manually push: git push -u origin main")
            return False
    else:
        print("\n⏸️  Upload paused. To push later, run:")
        print("   git push -u origin main")
        return True

def create_github_repository():
    """Instructions for creating GitHub repository"""
    print("\n📝 GitHub Repository Setup Instructions:")
    print("=" * 50)
    print("1. Go to https://github.com/new")
    print("2. Repository name: gitflow-ai")
    print("3. Description: 🤖 AI-Powered Git Workflow Assistant - Natural Language Git Interface")
    print("4. Make it Public (for hackathon visibility)")
    print("5. Don't initialize with README (we have one)")
    print("6. Click 'Create repository'")
    print("\n🏷️  Recommended topics to add:")
    print("   ai, git, assistant, openai, hackathon, python, flask, gpt, workflow")

def main():
    """Main function"""
    print("🤖 GitFlow AI - GitHub Upload Automation")
    print("👨‍💻 Author: Manav Sutar (sutarmanav557@gmail.com)")
    print("🏆 Built for OpenAI Hackathon")
    print()
    
    # Check if Git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git first.")
        return False
    
    # Show repository creation instructions
    create_github_repository()
    
    # Ask if repository is created
    response = input("\n❓ Have you created the GitHub repository? (y/n): ").lower().strip()
    
    if response not in ['y', 'yes']:
        print("⏸️  Please create the GitHub repository first, then run this script again.")
        return False
    
    # Set up and upload
    success = setup_git_repository()
    
    if success:
        print("\n🎊 GitFlow AI is now on GitHub!")
        print("🌟 Don't forget to star your own repository! ⭐")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)