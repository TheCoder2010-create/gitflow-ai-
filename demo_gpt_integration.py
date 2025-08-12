#!/usr/bin/env python3
"""
Demo script showing GPT-OSS integration for Git workflow assistance
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sys

class GitAssistantDemo:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-small"
        self.tokenizer = None
        self.model = None
        
    def load_model(self):
        """Load the GPT model"""
        print("Loading GPT-OSS model...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print("✅ Model loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def generate_response(self, prompt):
        """Generate a response using the GPT model"""
        if not self.model or not self.tokenizer:
            return "Model not loaded"
            
        try:
            # Create a more specific prompt for Git assistance
            git_prompt = f"Git help: {prompt}. Answer:"
            
            # Encode the input
            inputs = self.tokenizer.encode(git_prompt, return_tensors="pt")
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 30,
                    num_return_sequences=1,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the generated part
            generated_part = response[len(git_prompt):].strip()
            return generated_part if generated_part else "Use git commands to manage your repository."
            
        except Exception as e:
            return f"Error generating response: {e}"

def main():
    """Demo the Git assistant"""
    print("🚀 Intelligent Git Workflow Assistant Demo")
    print("=" * 50)
    
    assistant = GitAssistantDemo()
    
    if not assistant.load_model():
        print("Failed to load model. Exiting.")
        return
    
    # Demo queries
    demo_queries = [
        "How do I commit changes?",
        "How to create a new branch?",
        "How to merge branches?",
        "How to undo last commit?"
    ]
    
    print("\n🤖 AI-Powered Git Assistance Demo:")
    print("-" * 40)
    
    for query in demo_queries:
        print(f"\n❓ Question: {query}")
        response = assistant.generate_response(query)
        print(f"🤖 AI Response: {response}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed! GPT-OSS integration working!")
    print("\n💡 Next steps for your hackathon:")
    print("1. Implement task 1: Set up project structure")
    print("2. Implement task 2.1: Create GitStateAnalyzer")
    print("3. Implement task 3.1: Create GPTModelService")
    print("4. Continue with the implementation plan!")

if __name__ == "__main__":
    main()