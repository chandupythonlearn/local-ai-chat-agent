# DeepSeek Chat Application
# Version: 1.0.0

"""
Changelog:
- v1.0.0 (2024-02-02):
  * Initial release
  * Added model switching with confirmation
  * Added chat history clearing with confirmation
  * Implemented context length and temperature settings
  * Supported streaming responses from Ollama models

Future Roadmap:
- Add export/import chat history feature
- Implement persistent storage for chat sessions
- Add more advanced model configuration options
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime

# Configuration
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "deepseek-r1:14b"

# Application Version
APP_VERSION = "1.0.0"
APP_NAME = "DeepSeek Chat"

# Page setup
st.set_page_config(
    page_title=f"{APP_NAME} v{APP_VERSION}",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SessionState:
    @staticmethod
    def initialize():
        """Initialize session state with default values"""
        defaults = {
            'messages': [],
            'temperature': 0.7,
            'model': DEFAULT_MODEL,
            'current_chat_model': None,
            'context_length': 4096,
            'model_switch_requested': False,
            'requested_model': None,
            'clear_chat_requested': False
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @staticmethod
    def request_clear_chat():
        """Request to clear chat history"""
        st.session_state.clear_chat_requested = True
        st.rerun()

    @staticmethod
    def confirm_clear_chat():
        """Confirm and clear chat history"""
        st.session_state.messages = []
        st.session_state.current_chat_model = None
        st.session_state.clear_chat_requested = False
        st.rerun()

    @staticmethod
    def cancel_clear_chat():
        """Cancel clearing chat history"""
        st.session_state.clear_chat_requested = False
        st.rerun()

def get_available_models():
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        return []
    except:
        return []

def process_message(content: str) -> str:
    """Process message content, handling code blocks properly"""
    parts = []
    lines = content.split('\n')
    current_block = []
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith('```'):
            if in_code_block:
                if current_block:
                    code = '\n'.join(current_block)
                    parts.append('```python')
                    parts.append(code)
                    parts.append('```')
                current_block = []
                in_code_block = False
            else:
                if current_block:
                    parts.append('\n'.join(current_block))
                current_block = []
                in_code_block = True
        else:
            current_block.append(line)
    
    if current_block:
        if in_code_block:
            parts.append('```python')
            parts.append('\n'.join(current_block))
            parts.append('```')
        else:
            parts.append('\n'.join(current_block))
    
    return '\n'.join(parts)

def chat_stream(prompt: str):
    """Chat with the model with improved context handling"""
    conversation = []
    
    for msg in st.session_state.messages:
        conversation.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    conversation.append({
        "role": "user",
        "content": prompt
    })
    
    system_msg = {
        "role": "system",
        "content": "You are a helpful AI assistant. Maintain conversational context and provide consistent responses."
    }
    
    final_messages = [system_msg] + conversation
    
    payload = {
        "model": st.session_state.current_chat_model or st.session_state.model,
        "messages": final_messages,
        "stream": True,
        "options": {
            "temperature": st.session_state.temperature,
            "num_ctx": st.session_state.context_length
        }
    }
    
    try:
        with requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode())
                    if "message" in data:
                        yield data["message"]["content"]
    except Exception as e:
        yield f"Error: {str(e)}"

def main():
    # Initialize session state
    SessionState.initialize()
    
    # Sidebar
    with st.sidebar:
        st.title("Chat Settings")
        
        # Clear chat history with confirmation
        if st.session_state.clear_chat_requested:
            st.warning("Are you sure you want to clear the chat history?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm Clear", use_container_width=True):
                    SessionState.confirm_clear_chat()
            
            with col2:
                if st.button("Cancel", use_container_width=True):
                    SessionState.cancel_clear_chat()
            
            st.stop()
        
        # Model selection
        available_models = get_available_models()
        if available_models:
            # If a model switch was previously requested, show confirmation
            if st.session_state.model_switch_requested:
                st.warning("Are you sure you want to switch models? This will clear the current chat.")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Confirm Switch", use_container_width=True):
                        # Clear messages and switch model
                        st.session_state.messages = []
                        st.session_state.model = st.session_state.requested_model
                        st.session_state.current_chat_model = st.session_state.requested_model
                        st.session_state.model_switch_requested = False
                        st.session_state.requested_model = None
                        st.rerun()
                
                with col2:
                    if st.button("Cancel", use_container_width=True):
                        # Reset model switch request
                        st.session_state.model_switch_requested = False
                        st.session_state.requested_model = None
                        st.rerun()
                
                # Stop further rendering to show confirmation
                st.stop()
            
            # Model selection dropdown
            new_model = st.selectbox(
                "Select Model",
                available_models,
                index=available_models.index(st.session_state.model) if st.session_state.model in available_models else 0
            )
            
            # Check if model has changed
            if new_model != st.session_state.model:
                # Set up model switch request
                st.session_state.model_switch_requested = True
                st.session_state.requested_model = new_model
                st.rerun()
        
        # Temperature slider
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher values make the output more random, lower values more deterministic"
        )
        
        # Context length slider
        st.session_state.context_length = st.slider(
            "Context Length",
            min_value=512,
            max_value=8192,
            value=st.session_state.context_length,
            step=512,
            help="Number of tokens to use for context"
        )
        
        # Version information toggle
        st.sidebar.markdown("### App Information")
        version_expander = st.sidebar.expander(f"{APP_NAME} v{APP_VERSION}")
        with version_expander:
            st.markdown(f"**Version:** {APP_VERSION}")
            st.markdown("**Changelog:**")
            st.markdown("""
- v1.0.0:
  * Initial release
  * Model switching with confirmation
  * Chat history clearing with confirmation
  * Context length and temperature settings
  * Streaming responses from Ollama models
            """)
            
            st.markdown("**Roadmap:**")
            st.markdown("""
- Export/import chat history
- Persistent storage for chat sessions
- Advanced model configuration options
            """)
        
        # Chat context information
        if st.session_state.messages:
            st.markdown("### Chat Context")
            st.text(f"Messages in memory: {len(st.session_state.messages)}")
            st.text(f"Current Model: {st.session_state.current_chat_model}")
        
        # Clear chat history button
        if st.button("🧹 Clear Chat History", use_container_width=True):
            SessionState.request_clear_chat()
    
    # Main chat interface
    st.title(f"{APP_NAME} 🤖")
    st.caption("Powered by Ollama")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(process_message(msg["content"]))
            if msg["role"] == "assistant":
                st.markdown(f'<div class="model-badge">Model: {msg.get("model", st.session_state.current_chat_model)}</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Message DeepSeek..."):
        # Set current chat model if not set
        if not st.session_state.current_chat_model:
            st.session_state.current_chat_model = st.session_state.model
        
        # Add user message to session state
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            for chunk in chat_stream(prompt):
                full_response += chunk
                response_placeholder.markdown(process_message(full_response))
            
            # Add assistant message to session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response,
                "model": st.session_state.current_chat_model
            })
            
            # Display model badge
            st.markdown(f'<div class="model-badge">Model: {st.session_state.current_chat_model}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()