"""
Personality Module

Design Intent:
    This module manages response tone and styling independently from content
    generation (LLM) and conversation state (memory). By separating personality
    from other concerns, we enable:
    - Runtime personality switching without affecting conversation history
    - Consistent tone application regardless of LLM backend
    - Easy addition of new personality types
    
Key Design Decisions:
    - Strictly decoupled from LLM and memory (no dependencies on either)
    - Enum-based personality types for type safety and discoverability
    - Simple string manipulation for tone (no LLM needed for styling)
    - Trait-based approach allows easy customization and extension
"""

from typing import Dict, Any
from enum import Enum


class PersonalityTone(Enum):
    """Available personality tones."""
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    EMPATHETIC = "empathetic"
    ENTHUSIASTIC = "enthusiastic"


class PersonalityEngine:
    """
    Manages AI companion personality and response tone through trait-based styling.
    
    Design Intent:
        Applies consistent personality traits to responses without requiring LLM
        processing. This keeps personality application fast, predictable, and
        completely independent of the LLM module, enabling personality changes
        without regenerating content.
    """
    
    def __init__(self, tone: PersonalityTone = PersonalityTone.FRIENDLY):
        """
        Initialize personality engine with a specific tone.
        
        Design Rationale:
            Precomputes traits for the selected tone to make runtime application
            fast. Defaults to FRIENDLY tone to ensure welcoming user experience.
        
        Args:
            tone: Personality tone to use (from PersonalityTone enum)
        """
        self.tone = tone
        self.traits = self._get_traits()
        
    def _get_traits(self) -> Dict[str, str]:
        """
        Get personality traits for current tone from predefined templates.
        
        Design Rationale:
            Uses hardcoded trait mappings to avoid LLM dependency for personality.
            This makes personality application instant and deterministic, while
            keeping all trait definitions in one place for easy maintenance.
        
        Returns:
            Dictionary of personality traits (style, greeting, prefix, suffix)
        """
        trait_map = {
            PersonalityTone.FRIENDLY: {
                "style": "warm and approachable",
                "greeting": "Hey there!",
                "prefix": "I'd be happy to help! ",
                "suffix": " 😊"
            },
            PersonalityTone.PROFESSIONAL: {
                "style": "formal and precise",
                "greeting": "Hello,",
                "prefix": "Certainly. ",
                "suffix": ""
            },
            PersonalityTone.CASUAL: {
                "style": "relaxed and informal",
                "greeting": "Hey!",
                "prefix": "Sure thing! ",
                "suffix": " 👍"
            },
            PersonalityTone.EMPATHETIC: {
                "style": "understanding and supportive",
                "greeting": "Hello friend,",
                "prefix": "I understand. ",
                "suffix": " 💙"
            },
            PersonalityTone.ENTHUSIASTIC: {
                "style": "energetic and excited",
                "greeting": "Hi there!",
                "prefix": "Awesome question! ",
                "suffix": " ✨"
            }
        }
        return trait_map.get(self.tone, trait_map[PersonalityTone.FRIENDLY])
    
    def apply_tone(self, response: str, is_greeting: bool = False) -> str:
        """
        Apply personality tone to a response through string manipulation.
        
        Design Rationale:
            Uses simple prefix/suffix addition rather than LLM rewriting to keep
            the operation fast, predictable, and independent of LLM availability.
            This ensures personality works even in demo mode.
        
        Args:
            response: Original response text
            is_greeting: Whether this is a greeting message (uses different format)
            
        Returns:
            Response with personality tone applied
        """
        if is_greeting:
            return f"{self.traits['greeting']} {response}"
        
        # Apply prefix for first interaction or add subtle tone
        if not response.strip():
            return response
            
        # Add personality prefix and suffix
        styled_response = f"{self.traits['prefix']}{response}{self.traits['suffix']}"
        return styled_response
    
    def get_system_prompt(self) -> str:
        """
        Get system prompt describing the personality for LLM context.
        
        Design Rationale:
            Provides a way to inform the LLM about desired personality when
            generating responses, creating consistency between LLM-generated
            content and personality-styled output.
        
        Returns:
            System prompt string describing the personality traits
        """
        return f"You are a {self.traits['style']} AI companion. Respond in a {self.tone.value} manner."
    
    def set_tone(self, tone: PersonalityTone) -> None:
        """
        Change the personality tone.
        
        Args:
            tone: New personality tone
        """
        self.tone = tone
        self.traits = self._get_traits()


def create_personality(tone: str = "friendly") -> PersonalityEngine:
    """
    Factory function to create a personality engine.
    
    Args:
        tone: Personality tone name
        
    Returns:
        PersonalityEngine instance
    """
    try:
        tone_enum = PersonalityTone(tone.lower())
    except ValueError:
        tone_enum = PersonalityTone.FRIENDLY
    
    return PersonalityEngine(tone=tone_enum)
