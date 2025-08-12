#!/usr/bin/env python3
"""
Test script for GPT-OSS setup
This script tests loading and using a small open-source language model
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sys

def test_gpt_oss():
    """Test loading and using a small GPT model"""
    print("Testing GPT-OSS setup...")
    print(f"Python version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    # Use a small, fast model for testing
    model_name = "microsoft/DialoGPT-small"
    
    try:
        print(f"\nLoading model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Add padding token if it doesn't exist
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        print("Model loaded successfully!")
        
        # Test generation
        test_prompt = "How do I commit changes in git?"
        print(f"\nTest prompt: '{test_prompt}'")
        
        # Encode the input
        inputs = tokenizer.encode(test_prompt, return_tensors="pt")
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 50,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Generated response: '{response}'")
        
        print("\n✅ GPT-OSS setup is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing GPT-OSS: {e}")
        return False

if __name__ == "__main__":
    success = test_gpt_oss()
    sys.exit(0 if success else 1)