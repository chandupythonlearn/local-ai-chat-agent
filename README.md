# AI Chat Agent 🤖

A streamlit-based chat interface for Ollama models with support for multiple models, syntax highlighting, and context memory.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.24+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

<div align="center">
  <img src="docs/images/chat-interface.png" alt="Chat Interface" width="600"/>
</div>

## 🌟 Features

- 🤖 Support for multiple Ollama models
- 💡 Intelligent context memory
- 🎨 Syntax highlighting for code blocks
- 📋 Code copy functionality
- 🔄 Model switching with session management
- 🌡️ Temperature and context length control

## 🚀 Quick Start

1. **Prerequisites**
   - Python 3.8+
   - Ollama installed and running
   - Git

2. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/ai-chat-agent.git
   cd ai-chat-agent

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Start the Application**
   ```bash
   streamlit run src/chat_agent.py
   ```

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [User Guide](docs/user_guide.md)
- [Configuration Guide](docs/configuration.md)
- [Development Guide](docs/development.md)

## 🔧 Configuration

Basic configuration can be modified in `src/config.py`:
```python
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "deepseek-r1:14b"
```

See [configuration guide](docs/configuration.md) for more details.

## 🛠️ Development Setup

1. Create development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Run tests:
   ```bash
   pytest tests/
   ```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ollama team for their amazing model serving framework
- Streamlit team for the fantastic web framework

## 📞 Support

If you have any questions or run into issues, please:
1. Check the [documentation](docs/)
2. Look through [existing issues](https://github.com/yourusername/ai-chat-agent/issues)
3. Create a new issue if needed
