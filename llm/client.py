"""
LLM Client Module
Provides wrapper for Ollama-based language model interactions.
"""

import os
import requests
from typing import Optional, Dict, Any


class OllamaClient:
    """Wrapper for Ollama API interactions."""
    
    def __init__(self, base_url: Optional[str] = None, model: str = "llama2"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama API base URL (defaults to env var OLLAMA_BASE_URL or localhost)
            model: Model name to use (defaults to llama2)
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model
        
    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User input prompt
            context: Optional context to include
            
        Returns:
            Generated response text
        """
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: Unable to connect to Ollama (status {response.status_code})"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Please ensure Ollama is running."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """
        Check if Ollama service is available.
        
        Returns:
            True if Ollama is running and accessible
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False


def get_llm_client(model: str = "llama2") -> OllamaClient:
    """
    Factory function to get an LLM client instance.
    
    Args:
        model: Model name to use
        
    Returns:
        Configured OllamaClient instance
    """
    return OllamaClient(model=model)
