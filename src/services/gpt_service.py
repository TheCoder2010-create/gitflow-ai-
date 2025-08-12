"""
GPT-OSS model service for natural language processing
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Optional, Dict, Any
import logging
import time
from dataclasses import dataclass


@dataclass
class InferenceOptions:
    """Options for GPT model inference"""
    max_length: int = 512
    temperature: float = 0.7
    do_sample: bool = True
    top_p: float = 0.9
    top_k: int = 50
    num_return_sequences: int = 1
    pad_token_id: Optional[int] = None


class GPTModelService:
    """Service for managing GPT-OSS model interactions"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small", cache_dir: str = "./models"):
        """Initialize GPT model service"""
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.is_loaded = False
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def initialize(self, model_path: Optional[str] = None) -> bool:
        """Initialize and load the GPT model"""
        try:
            model_to_load = model_path or self.model_name
            
            self.logger.info(f"Loading GPT model: {model_to_load}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_to_load,
                cache_dir=self.cache_dir,
                trust_remote_code=True
            )
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_to_load,
                cache_dir=self.cache_dir,
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            # Move model to device
            self.model.to(self.device)
            
            # Set padding token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Set model to evaluation mode
            self.model.eval()
            
            self.is_loaded = True
            self.logger.info(f"Model loaded successfully on {self.device}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False
    
    def is_model_ready(self) -> bool:
        """Check if model is ready for inference"""
        return self.is_loaded and self.model is not None and self.tokenizer is not None
    
    def generate_response(self, prompt: str, options: Optional[InferenceOptions] = None) -> str:
        """Generate response using the GPT model"""
        if not self.is_model_ready():
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        if options is None:
            options = InferenceOptions()
        
        try:
            start_time = time.time()
            
            # Encode input
            inputs = self.tokenizer.encode(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=options.max_length // 2  # Leave room for generation
            ).to(self.device)
            
            # Set pad_token_id if not provided
            if options.pad_token_id is None:
                options.pad_token_id = self.tokenizer.eos_token_id
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=min(inputs.shape[1] + 100, options.max_length),
                    temperature=options.temperature,
                    do_sample=options.do_sample,
                    top_p=options.top_p,
                    top_k=options.top_k,
                    num_return_sequences=options.num_return_sequences,
                    pad_token_id=options.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    attention_mask=torch.ones_like(inputs)
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part
            generated_text = response[len(self.tokenizer.decode(inputs[0], skip_special_tokens=True)):].strip()
            
            inference_time = time.time() - start_time
            self.logger.debug(f"Generated response in {inference_time:.2f}s")
            
            return generated_text if generated_text else "I understand your request. Let me help you with that Git operation."
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return f"I encountered an error processing your request: {str(e)}"
    
    def generate_git_response(self, user_query: str, git_context: Dict[str, Any]) -> str:
        """Generate Git-specific response with context"""
        # Build context-aware prompt
        prompt = self._build_git_prompt(user_query, git_context)
        
        # Use specialized options for Git responses
        options = InferenceOptions(
            max_length=400,
            temperature=0.6,  # Lower temperature for more focused responses
            top_p=0.8
        )
        
        return self.generate_response(prompt, options)
    
    def _build_git_prompt(self, user_query: str, git_context: Dict[str, Any]) -> str:
        """Build a context-aware prompt for Git operations"""
        context_parts = []
        
        # Add repository state context
        if git_context.get("current_branch"):
            context_parts.append(f"Current branch: {git_context['current_branch']}")
        
        if git_context.get("staged_files"):
            staged_count = len(git_context["staged_files"])
            context_parts.append(f"Staged files: {staged_count}")
        
        if git_context.get("unstaged_files"):
            unstaged_count = len(git_context["unstaged_files"])
            context_parts.append(f"Modified files: {unstaged_count}")
        
        if git_context.get("untracked_files"):
            untracked_count = len(git_context["untracked_files"])
            context_parts.append(f"Untracked files: {untracked_count}")
        
        # Build the prompt
        context_str = " | ".join(context_parts) if context_parts else "Clean repository"
        
        prompt = f"""Git Assistant: I'm an AI that helps with Git operations.

Repository Status: {context_str}

User Question: {user_query}

Git Assistant Response:"""
        
        return prompt
    
    def generate_commit_message(self, diff_summary: str, file_changes: list) -> str:
        """Generate a commit message based on changes"""
        # Build prompt for commit message generation
        files_str = ", ".join(file_changes[:5])  # Limit to first 5 files
        if len(file_changes) > 5:
            files_str += f" and {len(file_changes) - 5} more files"
        
        prompt = f"""Generate a concise Git commit message for these changes:

Files changed: {files_str}
Summary: {diff_summary}

Commit message (use conventional commits format):"""
        
        options = InferenceOptions(
            max_length=200,
            temperature=0.5,  # Lower temperature for consistent commit messages
            top_p=0.7
        )
        
        response = self.generate_response(prompt, options)
        
        # Clean up the response to get just the commit message
        lines = response.strip().split('\n')
        commit_message = lines[0].strip()
        
        # Ensure it's not too long
        if len(commit_message) > 72:
            commit_message = commit_message[:69] + "..."
        
        return commit_message or "Update files"
    
    def cleanup(self):
        """Clean up model resources"""
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        # Clear CUDA cache if using GPU
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.is_loaded = False
        self.logger.info("Model resources cleaned up")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_model_ready():
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.model_name,
            "device": str(self.device),
            "vocab_size": self.tokenizer.vocab_size,
            "max_length": self.tokenizer.model_max_length,
            "parameters": sum(p.numel() for p in self.model.parameters()),
            "trainable_parameters": sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        }