import streamlit as st
import requests
import json
import time
from datetime import datetime

# Configuration
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "deepseek-r1:14b"

# Page setup
st.set_page_config(
    page_title="DeepSeek Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    if "model" not in st.session_state:
        st.session_state.model = DEFAULT_MODEL
    if "current_chat_model" not in st.session_state:
        st.session_state.current_chat_model = None
    if "show_model_switch_warning" not in st.session_state:
        st.session_state.show_model_switch_warning = False
    if "context_length" not in st.session_state:
        st.session_state.context_length = 4096

def handle_model_switch(new_model):
    """Handle model switching logic"""
    if st.session_state.messages and st.session_state.current_chat_model and new_model != st.session_state.current_chat_model:
        st.session_state.show_model_switch_warning = True
        return True
    st.session_state.current_chat_model = new_model
    st.session_state.show_model_switch_warning = False
    return False

def apply_styles():
    st.markdown("""
        <style>
            /* Code block container with lighter theme */
            pre {
                position: relative;
                padding: 2.5em 1em 1em 1em !important;
                margin: 1em 0;
                overflow: auto;
                background-color: #f8f8f8 !important;
                border-radius: 0.5em;
                border: 1px solid #e1e4e8;
            }

            /* Code text color */
            pre code {
                color: #24292e !important;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.6;
            }

            /* Updated copy button style */
            .copy-button {
                position: absolute;
                top: 8px;
                right: 8px;
                padding: 8px 16px;
                background-color: #0366d6;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 13px;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 6px;
                opacity: 1;
                transition: all 0.2s ease;
                z-index: 100;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .copy-button:hover {
                background-color: #0353b4;
                transform: translateY(-1px);
            }

            .copy-success {
                background-color: #28a745 !important;
            }

            /* Code block language badge */
            .code-language {
                position: absolute;
                top: 8px;
                left: 8px;
                padding: 4px 8px;
                background-color: #e1e4e8;
                color: #24292e;
                border-radius: 4px;
                font-size: 12px;
                font-family: monospace;
                font-weight: 500;
            }

            /* Syntax highlighting colors for light theme */
            .highlight .k { color: #d73a49; }  /* Keyword */
            .highlight .s { color: #032f62; }  /* String */
            .highlight .n { color: #24292e; }  /* Name */
            .highlight .o { color: #d73a49; }  /* Operator */
            .highlight .p { color: #24292e; }  /* Punctuation */
            .highlight .c1 { color: #6a737d; } /* Comment */
            .highlight .nb { color: #005cc5; } /* Built-in */
            .highlight .nf { color: #6f42c1; } /* Function */

            /* Message styling */
            .stChatMessage {
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            /* Model badge */
            .model-badge {
                background-color: #f1f8ff;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.8em;
                color: #0366d6;
                margin: 5px 0;
                border: 1px solid #c8e1ff;
            }

            /* Context counter */
            .context-counter {
                color: #666;
                font-size: 0.9em;
                margin-top: 5px;
            }
        </style>
        
        <script>
        function copyCode(button) {
            const codeBlock = button.parentElement;
            const code = codeBlock.querySelector('code') || codeBlock.querySelector('pre');
            const textToCopy = code.innerText;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                button.innerHTML = '✓ Copied!';
                button.classList.add('copy-success');
                setTimeout(() => {
                    button.innerHTML = '📋 Copy';
                    button.classList.remove('copy-success');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
                button.innerHTML = '❌ Error';
                setTimeout(() => {
                    button.innerHTML = '📋 Copy';
                }, 2000);
            });
        }
        
        function addCopyButtons() {
            document.querySelectorAll('pre').forEach((block) => {
                if (!block.querySelector('.copy-button')) {
                    const button = document.createElement('button');
                    button.className = 'copy-button';
                    button.innerHTML = '📋 Copy';
                    button.onclick = function() { copyCode(this); };
                    
                    const lang = document.createElement('span');
                    lang.className = 'code-language';
                    lang.textContent = 'Python';
                    
                    block.insertBefore(lang, block.firstChild);
                    block.insertBefore(button, block.firstChild);
                }
            });
        }

        document.addEventListener('DOMContentLoaded', addCopyButtons);
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes.length) {
                    addCopyButtons();
                }
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
    """, unsafe_allow_html=True)

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
    # Build complete conversation history
    conversation = []
    
    # Add previous messages to maintain context
    for msg in st.session_state.messages:
        conversation.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add current message
    conversation.append({
        "role": "user",
        "content": prompt
    })
    
    # Add system message for context
    system_msg = {
        "role": "system",
        "content": "You are a helpful AI assistant. Maintain conversational context and provide consistent responses."
    }
    
    # Combine all messages
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

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.messages = []
    st.session_state.current_chat_model = None
    st.rerun()

def main():
    initialize_session_state()
    apply_styles()
    
    # Sidebar
    with st.sidebar:
        st.title("Chat Settings")
        
        # Model selection with warning
        available_models = get_available_models()
        if available_models:
            previous_model = st.session_state.model
            new_model = st.selectbox(
                "Select Model",
                available_models,
                index=available_models.index(st.session_state.model) if st.session_state.model in available_models else 0
            )
            
            if new_model != previous_model:
                if handle_model_switch(new_model):
                    st.warning("⚠️ Switching models will start a new chat. Current chat history will be cleared.")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Confirm", use_container_width=True):
                            st.session_state.messages = []
                            st.session_state.model = new_model
                            st.session_state.current_chat_model = new_model
                            st.session_state.show_model_switch_warning = False
                            st.rerun()
                    with col2:
                        if st.button("❌ Cancel", use_container_width=True):
                            st.session_state.model = previous_model
                            st.session_state.show_model_switch_warning = False
                            st.rerun()
                else:
                    st.session_state.model = new_model
        
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher values make the output more random, lower values more deterministic"
        )
        
        st.session_state.context_length = st.slider(
            "Context Length",
            min_value=512,
            max_value=8192,
            value=st.session_state.context_length,
            step=512,
            help="Number of tokens to use for context"
        )
        
        if st.session_state.messages:
            st.markdown("### Chat Context")
            st.text(f"Messages in memory: {len(st.session_state.messages)}")
            st.text(f"Current Model: {st.session_state.current_chat_model}")
        
        if st.button("🧹 Clear Chat History", use_container_width=True):
            clear_chat_history()
    
    # Main chat interface
    st.title("DeepSeek Chat 🤖")
    st.caption("Powered by Ollama")
    
    if st.session_state.show_model_switch_warning:
        st.warning("Please confirm or cancel the model switch in the sidebar")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(process_message(msg["content"]))
            if msg["role"] == "assistant":
                st.markdown(f'<div class="model-badge">Model: {msg.get("model", st.session_state.current_chat_model)}</div>', unsafe_allow_html=True)
    
    # Chat input
    if not st.session_state.show_model_switch_warning:
        if prompt := st.chat_input("Message DeepSeek..."):
            if not st.session_state.current_chat_model:
                st.session_state.current_chat_model = st.session_state.model
            
            st.session_state.messages.append({
                "role": "user", 
                "content": prompt
            })
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in chat_stream(prompt):
                    full_response += chunk
                    response_placeholder.markdown(process_message(full_response))
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response,
                    "model": st.session_state.current_chat_model
                })
                st.markdown(f'<div class="model-badge">Model: {st.session_state.current_chat_model}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()