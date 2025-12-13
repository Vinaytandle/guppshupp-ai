"""
Memory Module

Design Intent:
    This module manages conversation history independently from LLM and
    personality logic. By maintaining a separate memory system, we enable:
    - Conversation continuity across multiple exchanges
    - Context extraction for improved LLM responses
    - Future extensions like persistence or advanced memory retrieval
    
Key Design Decisions:
    - Strictly decoupled from LLM and personality modules (no dependencies)
    - Placeholder implementations for topic extraction (simple but extensible)
    - Configurable history limits to manage memory usage
    - Timestamp tracking for potential future time-aware features
"""

from typing import List, Dict, Any
from datetime import datetime


class ConversationMemory:
    """
    Manages conversation history and memory extraction.
    
    Design Intent:
        Provides a centralized store for conversation state that is completely
        independent of how messages are generated (LLM) or styled (personality).
        This separation allows each component to evolve independently and makes
        testing easier.
    """
    
    def __init__(self, max_history: int = 10):
        """
        Initialize conversation memory with bounded storage.
        
        Design Rationale:
            Limits history size to prevent unbounded memory growth while
            keeping recent context for meaningful conversations. The sliding
            window approach is simple and predictable.
        
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
        Extract key topics from conversation history using simple heuristics.
        
        Design Rationale:
            Uses placeholder logic (word length filtering) to demonstrate the
            concept without adding NLP library dependencies. This keeps the
            project minimal while showing where advanced topic modeling could
            be added in the future.
        
        Returns:
            List of identified topics (currently simple keyword extraction)
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
        Get a summary of the conversation with basic statistics.
        
        Design Rationale:
            Provides a simple text summary without requiring LLM-based
            summarization. This demonstrates the summary concept while keeping
            dependencies minimal and execution fast.
        
        Returns:
            Conversation summary with message count and topics
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
