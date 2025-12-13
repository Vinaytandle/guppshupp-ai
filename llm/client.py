"""
LLM Client Module

Design Intent:
    This module provides a thin wrapper around the Ollama API to decouple
    the application from specific LLM implementation details. By abstracting
    the LLM interaction, we enable easy substitution of different backends
    and provide graceful degradation when Ollama is unavailable.

Key Design Decisions:
    - Configuration via environment variables to avoid hardcoded secrets
    - Optional LLM with automatic fallback to ensure app works without Ollama
    - Specific exception handling to distinguish connection vs. other errors
"""

import os
import requests
from typing import Optional, Dict, Any


class OllamaClient:
    """
    Wrapper for Ollama API interactions.
    
    Design Intent:
        Encapsulates all Ollama-specific communication logic, providing a clean
        interface for the rest of the application. This abstraction allows the
        app to remain functional even when Ollama is not available, supporting
        both production and demo/development scenarios.
    """
    
    def __init__(self, base_url: Optional[str] = None, model: str = "llama2"):
        """
        Initialize Ollama client with configurable endpoint.
        
        Design Rationale:
            Uses environment variable fallback to avoid hardcoding URLs while
            allowing override for testing or different deployment scenarios.
        
        Args:
            base_url: Ollama API base URL (defaults to env var OLLAMA_BASE_URL or localhost)
            model: Model name to use (defaults to llama2)
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model
        
    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a response from the LLM with graceful error handling.
        
        Design Rationale:
            Returns error messages as strings rather than raising exceptions,
            allowing the UI to display meaningful feedback to users when LLM
            is unavailable. This keeps the application functional in degraded mode.
        
        Args:
            prompt: User input prompt
            context: Optional context to include (for conversation continuity)
            
        Returns:
            Generated response text or user-friendly error message
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
        Check if Ollama service is available without raising exceptions.
        
        Design Rationale:
            Provides a simple boolean check to enable conditional logic in the
            UI (e.g., showing demo mode vs. full LLM functionality). Catches all
            exceptions to ensure the check never crashes the application.
        
        Returns:
            True if Ollama is running and accessible, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False


def get_llm_client(model: str = "llama2") -> OllamaClient:
    """
    Factory function to get an LLM client instance.
    
    Design Rationale:
        Provides a simple creation interface that could be extended in the future
        to select different LLM backends based on configuration, while keeping
        the current implementation minimal and focused on Ollama.
    
    Args:
        model: Model name to use (allows testing with different Ollama models)
        
    Returns:
        Configured OllamaClient instance
    """
    return OllamaClient(model=model)
