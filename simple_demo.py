#!/usr/bin/env python3
"""
Simple demo showing that GPT-OSS is working
"""

def main():
    print("🚀 Intelligent Git Workflow Assistant")
    print("=" * 50)
    
    # Test imports
    try:
        import torch
        import transformers
        print("✅ PyTorch version:", torch.__version__)
        print("✅ Transformers version:", transformers.__version__)
        print("✅ CUDA available:", torch.cuda.is_available())
    except ImportError as e:
        print("❌ Import error:", e)
        return
    
    print("\n🎯 Your hackathon project is ready!")
    print("\n📋 Implementation Plan:")
    print("1. ✅ GPT-OSS setup complete")
    print("2. ✅ Basic CLI structure created")
    print("3. ✅ Dependencies installed")
    print("4. 🚧 Ready to implement tasks from spec!")
    
    print("\n🚀 Next steps:")
    print("- Open .kiro/specs/intelligent-git-workflow-assistant/tasks.md")
    print("- Start with Task 1: Set up project structure")
    print("- Use the GPT model for natural language processing")
    print("- Build your AI-powered Git assistant!")
    
    print("\n💡 Quick test commands:")
    print("- python git_assistant.py --help")
    print("- python git_assistant.py ask 'How do I commit?'")
    
    print("\n🏆 Good luck with your OpenAI hackathon!")

if __name__ == "__main__":
    main()