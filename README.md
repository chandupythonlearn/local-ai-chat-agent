# AI Chat Agent 🤖 - Powered by Ollama

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.24+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blueviolet.svg)

## 🚀 Discover Conversational AI at Your Fingertips

Transform your local machine into an intelligent conversational powerhouse with our cutting-edge AI Chat Agent! Harness the power of Ollama models right from your desktop.

## 🌟 What's New in v1.0.0

### Major Features
- 🤖 Multi-model support
- 💡 Intelligent context management
- 🎨 Advanced code block handling
- 🔄 Seamless model switching

### Version Highlights
- Initial release of the AI Chat Agent
- Robust Ollama model integration
- Intuitive user interface
- Flexible conversation controls

## 📋 Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- Ollama installed and running ([Ollama Installation Guide](https://github.com/ollama/ollama))
- Git (optional, for cloning)

## 🚀 Installation

1. **Get the Code**
   ```bash
   # Option 1: Clone with git
   git clone https://github.com/yourusername/local-ai-chat-agent.git
   cd local-ai-chat-agent

   # Option 2: Download ZIP
   # Download and extract the ZIP file
   cd local-ai-chat-agent
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Required Models**
   ```bash
   # Make sure Ollama is running
   ollama serve

   # In another terminal, pull models
   ollama pull deepseek-r1:14b
   # Optional: Pull additional models
   ollama pull llama2
   ollama pull mistral
   ```

## 💻 Usage

1. **Start Ollama Server** (if not already running)
   ```bash
   ollama serve
   ```

2. **Launch the Chat Interface**
   ```bash
   streamlit run src/chat_agent.py
   ```

3. **Access the Interface**
   - Open your browser to `http://localhost:8501`
   - Select your preferred model from the sidebar
   - Start chatting!

## 🌠 Version Roadmap

### Upcoming in v1.1.0
- [ ] Export/import chat history
- [ ] Enhanced model performance metrics
- [ ] Additional UI customization options
- [ ] Persistent chat session storage

### Future Vision (v1.2.0+)
- Advanced prompt engineering tools
- Multi-language support
- Integration with local knowledge bases
- Advanced analytics dashboard

## 🛠️ Features Guide

### Model Selection
- Choose models from the dropdown in sidebar
- Switching models requires confirmation
- Each chat session maintains its own context

### Temperature Control
- Adjust from 0.0 to 1.0
- Lower values (0.1-0.3): More focused, deterministic responses
- Higher values (0.7-1.0): More creative, varied responses

### Code Block Features
- Automatic syntax highlighting
- Copy button for easy code copying
- Support for multiple programming languages

### Context Memory
- Maintains conversation history
- Remembers previous interactions
- Clear context with "Clear Chat History" button

## 📊 Version History

### v1.0.0 (2024-02-02)
- 🎉 Initial public release
- Implemented core chat functionality
- Added model switching mechanism
- Integrated context and temperature controls
- Developed robust error handling

### Planned Versions
- **v1.1.0**: Enhanced user experience
- **v1.2.0**: Advanced AI capabilities
- **v1.3.0**: Enterprise-grade features

## ⚙️ Configuration

Default settings can be modified at runtime through the UI:
- Model selection
- Temperature
- Context length

## 🔍 Troubleshooting

### Common Issues

1. **"Ollama Not Connected" Error**
   ```bash
   # Check if Ollama is running
   ollama list
   # Start if needed
   ollama serve
   ```

2. **"Model Not Found" Error**
   ```bash
   # Pull the required model
   ollama pull model-name
   ```

3. **Memory Issues**
   - Reduce context length in sidebar
   - Clear chat history
   - Restart application

## 📖 Tips for Best Results

1. **Model Selection**
   - Use smaller models for quick responses
   - Use larger models for complex tasks
   - Match model to task requirements

2. **Temperature Settings**
   - Use 0.1-0.3 for precise, factual responses
   - Use 0.4-0.6 for balanced responses
   - Use 0.7-1.0 for creative tasks

3. **Context Management**
   - Clear chat history for new topics
   - Adjust context length as needed
   - Monitor memory usage

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting guide above
2. Create an issue in the GitHub repository
3. Provide detailed information about your problem

---

Made with ❤️ by [Chandra]