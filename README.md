# Ailemdar 

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-blue?logo=github-actions)](https://github.com/omerfdmrl)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://github.com/omerfdmrl)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/omerfdmrl)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://github.com/omerfdmrl)

> **Your Intelligent AI Software Engineering Assistant** 
> 
> Automated PR reviews and issue resolution powered by state-of-the-art LLMs

---

## ✨ Features

- **🤖 AI-Powered PR Reviews** - Get intelligent code reviews with inline comments, identifying bugs, security issues, and improvements
- **🔧 Automatic Issue Resolution** - Analyzes GitHub issues and automatically creates fixes with pull requests
- **🎯 Multi-LLM Support** - Works with OpenAI, Anthropic Claude, Google Gemini, Ollama (local), and custom endpoints
- **🔍 Smart Context Management** - Vector-based code search using FAISS for understanding large codebases
- **⚡ Fast & Efficient** - Local embeddings support for reduced API costs and faster processing
- **🛡️ Security First** - Built-in security checks and safe code modification practices
- **📊 Structured Logging** - Comprehensive observability with structured JSON logging
- **🐳 Docker Ready** - Containerized for easy deployment as GitHub Action or standalone service

---

## 🚀 Quick Start

### Using as GitHub Action

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]
  issues:
    types: [opened, labeled]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: AI Code Review
        uses: your-org/ailemdar@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          llm_provider: openai
          llm_model: gpt-4o
          llm_api_key: ${{ secrets.OPENAI_API_KEY }}
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/your-org/ailemdar.git
cd ailemdar

# Setup virtual environment and install dependencies
make setup-venv
source venv/bin/activate

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run tests
make test

# Start development server
make dev
```

---

## 📋 Requirements

- **Python**: 3.11 or higher
- **GitHub Token**: For repository access
- **LLM API Key**: OpenAI, Anthropic, Google, or custom provider
- **Docker**: (optional) For containerized deployment

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GITHUB_TOKEN` | GitHub API token | Yes | - |
| `LLM_PROVIDER` | LLM provider (openai, anthropic, gemini, ollama) | No | openai |
| `LLM_MODEL` | Model name (e.g., gpt-4o, claude-3-5-sonnet) | No | gpt-4o |
| `LLM_API_KEY` | API key for LLM provider | Yes* | - |
| `LLM_BASE_URL` | Custom endpoint URL (for Ollama/self-hosted) | No** | - |
| `ENABLE_LIN