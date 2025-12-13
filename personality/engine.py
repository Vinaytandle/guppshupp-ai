"""
Personality Module
Manages response tone and personality traits for the AI companion.
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
    """Manages AI companion personality and response tone."""
    
    def __init__(self, tone: PersonalityTone = PersonalityTone.FRIENDLY):
        """
        Initialize personality engine.
        
        Args:
            tone: Personality tone to use
        """
        self.tone = tone
        self.traits = self._get_traits()
        
    def _get_traits(self) -> Dict[str, str]:
        """
        Get personality traits for current tone.
        
        Returns:
            Dictionary of personality traits
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
        Apply personality tone to a response.
        
        Args:
            response: Original response text
            is_greeting: Whether this is a greeting message
            
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
        Get system prompt that describes the personality.
        
        Returns:
            System prompt string
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
