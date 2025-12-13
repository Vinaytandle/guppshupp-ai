"""
GuppShupp AI - AI Companion Demo
A minimal Streamlit application demonstrating an AI companion with personality.
"""

import streamlit as st
import json
import os
from pathlib import Path

from llm import get_llm_client
from memory import create_memory
from personality import create_personality, PersonalityTone


# Page configuration
st.set_page_config(
    page_title="GuppShupp AI Companion",
    page_icon="🤖",
    layout="centered"
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "memory" not in st.session_state:
        st.session_state.memory = create_memory(max_history=20)
    
    if "personality" not in st.session_state:
        st.session_state.personality = create_personality("friendly")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "llm_client" not in st.session_state:
        st.session_state.llm_client = get_llm_client()


def load_sample_data():
    """Load sample chat data if available."""
    sample_file = Path(__file__).parent / "data" / "sample_chat.json"
    
    if sample_file.exists():
        try:
            with open(sample_file, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading sample data: {e}")
    
    return []


def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Personality selection
        st.subheader("Personality Tone")
        tone_options = [tone.value for tone in PersonalityTone]
        selected_tone = st.selectbox(
            "Select AI personality",
            tone_options,
            index=tone_options.index(st.session_state.personality.tone.value)
        )
        
        if selected_tone != st.session_state.personality.tone.value:
            st.session_state.personality = create_personality(selected_tone)
            st.success(f"Personality changed to {selected_tone}")
        
        st.divider()
        
        # LLM configuration
        st.subheader("LLM Configuration")
        ollama_status = st.session_state.llm_client.is_available()
        
        if ollama_status:
            st.success("✅ Ollama connected")
        else:
            st.warning("⚠️ Ollama not available")
            st.info("Using demo mode. Install Ollama for full functionality.")
        
        st.divider()
        
        # Memory stats
        st.subheader("Memory Stats")
        st.metric("Messages in history", len(st.session_state.memory.history))
        
        if st.session_state.memory.history:
            st.text("Recent topics:")
            topics = st.session_state.memory.extract_topics()
            for topic in topics[:3]:
                st.text(f"• {topic}")
        
        st.divider()
        
        # Load sample data
        if st.button("📥 Load Sample Chat"):
            sample_data = load_sample_data()
            if sample_data:
                st.session_state.messages = sample_data
                for msg in sample_data:
                    st.session_state.memory.add_message(msg["role"], msg["content"])
                st.success("Sample data loaded!")
                st.rerun()
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.session_state.memory.clear()
            st.success("Conversation cleared!")
            st.rerun()


def generate_response(prompt: str) -> str:
    """
    Generate a response using the LLM with personality and context.
    
    Args:
        prompt: User input
        
    Returns:
        AI response
    """
    # Get conversation context
    context = st.session_state.memory.get_context(num_messages=5)
    
    # Get personality system prompt
    system_prompt = st.session_state.personality.get_system_prompt()
    
    # Combine context and system prompt
    full_context = f"{system_prompt}\n\nRecent conversation:\n{context}" if context else system_prompt
    
    # Check if Ollama is available
    if st.session_state.llm_client.is_available():
        # Generate response using Ollama
        response = st.session_state.llm_client.generate(prompt, context=full_context)
    else:
        # Demo mode: provide a placeholder response
        response = "This is a demo response. Connect to Ollama for real AI interactions!"
    
    # Apply personality tone
    styled_response = st.session_state.personality.apply_tone(response)
    
    return styled_response


def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Main header
    st.title("🤖 GuppShupp AI Companion")
    st.markdown("*Your friendly AI companion for conversations*")
    
    st.divider()
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.memory.add_message("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
            st.markdown(response)
        
        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.memory.add_message("assistant", response)


if __name__ == "__main__":
    main()
