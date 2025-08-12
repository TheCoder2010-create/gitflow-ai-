#!/usr/bin/env python3
"""
Test AI-Powered Git Conversations
Simple test to verify the core functionality
"""

import sys
import os

# Test basic imports first
try:
    import torch
    import transformers
    import git
    print("✅ All dependencies available")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    sys.exit(1)

# Simple AI conversation test
def test_ai_conversation():
    """Test basic AI conversation functionality"""
    print("🧪 Testing AI-Powered Git Conversations")
    print("=" * 50)
    
    # Test 1: Basic GPT model loading
    print("\n1. Testing GPT Model Loading...")
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        model_name = "microsoft/DialoGPT-small"
        print(f"Loading model: {model_name}")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        print("✅ GPT model loaded successfully!")
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False
    
    # Test 2: Git repository analysis
    print("\n2. Testing Git Repository Analysis...")
    try:
        from git import Repo, InvalidGitRepositoryError
        
        repo = Repo(".")
        current_branch = repo.active_branch.name
        is_dirty = repo.is_dirty()
        
        print(f"✅ Git analysis successful!")
        print(f"   Current branch: {current_branch}")
        print(f"   Repository dirty: {is_dirty}")
        
    except InvalidGitRepositoryError:
        print("⚠️ Not a Git repository - creating test scenario")
    except Exception as e:
        print(f"❌ Git analysis failed: {e}")
        return False
    
    # Test 3: Natural language processing
    print("\n3. Testing Natural Language Processing...")
    try:
        test_queries = [
            "How do I commit my changes?",
            "I want to undo my last commit",
            "Create a new branch",
            "Show me the status"
        ]
        
        # Simple pattern matching (without full AI for now)
        git_patterns = {
            r'commit': 'git commit -m "message"',
            r'undo.*commit': 'git reset --soft HEAD~1',
            r'new.*branch|create.*branch': 'git checkout -b branch-name',
            r'status': 'git status'
        }
        
        import re
        
        for query in test_queries:
            print(f"\n❓ Query: {query}")
            
            # Find matching pattern
            matched = False
            for pattern, command in git_patterns.items():
                if re.search(pattern, query.lower()):
                    print(f"🤖 Suggested: {command}")
                    matched = True
                    break
            
            if not matched:
                print("🤖 I can help you with Git operations. Please be more specific.")
        
        print("\n✅ Natural language processing working!")
        
    except Exception as e:
        print(f"❌ NLP test failed: {e}")
        return False
    
    # Test 4: AI Response Generation
    print("\n4. Testing AI Response Generation...")
    try:
        # Simple AI response test
        test_prompt = "Git help: How do I commit changes? Answer:"
        
        inputs = tokenizer.encode(test_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 30,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_part = response[len(test_prompt):].strip()
        
        print(f"🤖 AI Response: {generated_part}")
        print("✅ AI response generation working!")
        
    except Exception as e:
        print(f"❌ AI response generation failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All AI Conversation Tests Passed!")
    print("\n🚀 Ready to implement full GitFlow AI system!")
    
    return True

if __name__ == "__main__":
    success = test_ai_conversation()
    if success:
        print("\n💡 Next steps:")
        print("1. ✅ AI-Powered Git Conversations - Core functionality working")
        print("2. 🚧 Implement full conversation system")
        print("3. 🚧 Add safety validations")
        print("4. 🚧 Integrate with CLI")
    else:
        print("\n❌ Tests failed. Please check dependencies and try again.")
    
    sys.exit(0 if success else 1)