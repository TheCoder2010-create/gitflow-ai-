# GitFlow AI - Intelligent Git Workflow Assistant

🤖 **AI-Powered Git Conversations** | Transform your Git experience with natural language assistance

Built for the **OpenAI Hackathon** - An intelligent Git workflow assistant that understands natural language and provides smart Git command suggestions.

![GitFlow AI Demo](https://img.shields.io/badge/Status-Live%20Demo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13+-blue)
![AI](https://img.shields.io/badge/AI-GPT--OSS-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

### ✨ **AI-Powered Git Conversations**
- **Natural Language Interface**: Ask questions like "How do I commit my changes?" or "I want to undo my last commit"
- **Context-Aware Suggestions**: AI understands your repository state and provides personalized advice
- **Safety Validations**: Prevents destructive operations with intelligent warnings
- **Interactive Chat**: Real-time conversations with your AI Git assistant

### 🧠 **Smart Git Operations**
- **Intelligent Commit Messages**: AI analyzes code changes and generates meaningful commit messages
- **Workflow Detection**: Automatically detects GitFlow, GitHub Flow, and other workflows
- **Branch Management**: Smart suggestions for creating, merging, and managing branches
- **Conflict Resolution**: AI-guided merge conflict resolution

### 🛡️ **Safety & Reliability**
- **Risk Assessment**: Commands are categorized as safe, moderate, or destructive
- **Confirmation Prompts**: Destructive operations require explicit confirmation
- **Alternative Suggestions**: Safer alternatives for risky operations
- **Rollback Guidance**: Help with undoing operations when needed

## 🎯 Quick Start

### Prerequisites
- Python 3.13+
- Git repository
- Internet connection (for AI model download)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/TheCoder2010-create/gitflow-ai-.git
cd gitflow-ai-
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize GitFlow AI**
```bash
python gitflow_cli.py init
```

### Usage

#### Command Line Interface
```bash
# Ask AI about Git operations
python gitflow_cli.py ask "How do I commit my changes?"

# Interactive conversation mode
python gitflow_cli.py ask --interactive

# Get enhanced Git status
python gitflow_cli.py status

# Run demo
python gitflow_cli.py demo
```

#### Web Interface
```bash
# Start the web server
python web/api.py

# Open browser to http://localhost:5000
```

## 🌐 Web Interface

The web interface provides a beautiful, interactive experience:

- **Landing Page**: Professional SaaS-style presentation
- **AI Chat Modal**: Real-time conversations with the AI assistant
- **Interactive Demos**: Click feature cards to try functionality
- **Quick Actions**: Common Git operations at your fingertips

### API Endpoints

- `POST /api/ask` - AI conversation endpoint
- `GET /api/status` - Repository status
- `POST /api/commit` - Commit message generation
- `GET /api/demo` - Demo conversations
- `GET /api/health` - Health check

## 🏗️ Architecture

```
GitFlow AI/
├── src/
│   └── gitflow_ai.py          # Core AI system
├── web/
│   ├── index.html             # Landing page
│   ├── styles.css             # Styling
│   ├── script.js              # Frontend logic
│   └── api.py                 # Flask API server
├── .kiro/specs/               # Project specifications
├── gitflow_cli.py             # CLI interface
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

### Core Components

1. **GitStateAnalyzer**: Analyzes repository state
2. **GPTModelService**: Manages AI model interactions
3. **GitCommandParser**: Parses natural language to Git commands
4. **SimpleGitAI**: Main conversation system
5. **Flask API**: Web service layer
6. **Interactive Frontend**: Modern web interface

## 🧪 Testing

### Run Tests
```bash
# Test AI conversation system
python test_ai_conversation.py

# Test API integration
python test_api_integration.py

# Test CLI functionality
python gitflow_cli.py demo
```

### Example Conversations

**User**: "How do I commit my changes?"
**AI**: I understand you want to commit your staged changes. Here's what I suggest:
- ✅ `git commit -m "your message"` - This will create a new commit with your staged changes.

**User**: "I want to undo my last commit but keep the changes"
**AI**: I understand you want to undo the last commit while preserving your changes:
- 🚨 `git reset --soft HEAD~1` - This removes the last commit but keeps your changes in the staging area.
- ⚠️ Warning: This is a destructive operation!

## 🎨 Screenshots

### Landing Page
![Landing Page](docs/landing-page.png)

### AI Chat Interface
![AI Chat](docs/ai-chat.png)

### CLI Interface
![CLI Demo](docs/cli-demo.png)

## 🚀 Deployment

### Local Development
```bash
python web/api.py
```

### Production Deployment
- **Vercel**: Deploy the web folder
- **Heroku**: Use the included Procfile
- **Docker**: Containerized deployment ready

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Hackathon Project

This project was built for the **OpenAI Hackathon** to demonstrate:
- **AI-Powered Developer Tools**: Natural language interfaces for technical tasks
- **GPT-OSS Integration**: Using open-source language models effectively
- **User Experience**: Making complex Git operations accessible to all developers
- **Safety & Reliability**: AI systems that prevent user errors

## 🔗 Links

- **Live Demo**: [GitFlow AI Demo](https://gitflow-ai.vercel.app)
- **Documentation**: [Full Docs](docs/README.md)
- **API Reference**: [API Docs](docs/api.md)
- **Hackathon Submission**: [OpenAI Hackathon](https://openai-hackathon.com)

## 👨‍💻 Author

**Manav Sutar**
- GitHub: [@TheCoder2010-create](https://github.com/TheCoder2010-create)
- Email: sutarmanav557@gmail.com

## 🙏 Acknowledgments

- OpenAI for the hackathon opportunity
- Hugging Face for transformer models
- The open-source community for amazing tools
- Git for being the foundation of modern development

---

**Built with ❤️ for developers who want to Git things done faster!** 🚀