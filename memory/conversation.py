"""
Memory Module
Handles extraction and management of conversation memory.
"""

from typing import List, Dict, Any
from datetime import datetime


class ConversationMemory:
    """Manages conversation history and memory extraction."""
    
    def __init__(self, max_history: int = 10):
        """
        Initialize conversation memory.
        
        Args:
            max_history: Maximum number of messages to keep in history
        """
        self.max_history = max_history
        self.history: List[Dict[str, Any]] = []
        
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to conversation history.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(message)
        
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self, num_messages: int = 5) -> str:
        """
        Get recent conversation context.
        
        Args:
            num_messages: Number of recent messages to include
            
        Returns:
            Formatted context string
        """
        recent = self.history[-num_messages:] if self.history else []
        context_parts = []
        
        for msg in recent:
            role = msg["role"].capitalize()
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def extract_topics(self) -> List[str]:
        """
        Extract key topics from conversation history.
        
        Returns:
            List of identified topics (placeholder implementation)
        """
        # Placeholder: In a real implementation, this would use NLP/LLM
        # to extract meaningful topics from the conversation
        topics = []
        
        for msg in self.history:
            if msg["role"] == "user":
                # Simple keyword extraction (placeholder)
                words = msg["content"].lower().split()
                topics.extend([w for w in words if len(w) > 5])
        
        # Return unique topics
        return list(set(topics))[:5]
    
    def get_summary(self) -> str:
        """
        Get a summary of the conversation.
        
        Returns:
            Conversation summary (placeholder implementation)
        """
        if not self.history:
            return "No conversation history"
        
        num_messages = len(self.history)
        topics = self.extract_topics()
        
        summary = f"Conversation with {num_messages} messages"
        if topics:
            summary += f", discussing: {', '.join(topics[:3])}"
        
        return summary
    
    def clear(self) -> None:
        """Clear all conversation history."""
        self.history = []


def create_memory(max_history: int = 10) -> ConversationMemory:
    """
    Factory function to create a conversation memory instance.
    
    Args:
        max_history: Maximum messages to keep
        
    Returns:
        ConversationMemory instance
    """
    return ConversationMemory(max_history=max_history)
