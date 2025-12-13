# GuppShupp AI - AI Companion Demo

A minimal Python Streamlit application demonstrating an AI companion with personality, memory, and LLM integration.

## 🏗️ Architecture

This project follows a clean, modular architecture with the following components:

```
guppshupp-ai/
├── app.py                 # Main Streamlit application entry point
├── llm/                   # LLM client wrapper module
│   ├── __init__.py
│   └── client.py          # Ollama-based LLM client
├── memory/                # Conversation memory module
│   ├── __init__.py
│   └── conversation.py    # Memory extraction and management
├── personality/           # Response tone engine module
│   ├── __init__.py
│   └── engine.py          # Personality and tone configuration
├── data/                  # Sample chat data
│   ├── sample_chat.json   # Example conversations
│   └── README.md
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

### Module Descriptions

#### 🤖 LLM Module (`llm/`)
- **Purpose**: Provides a wrapper for Ollama-based language model interactions
- **Key Features**:
  - Ollama API integration with configurable endpoint
  - Error handling and connection status checking
  - Context-aware prompt generation
  - No hardcoded API keys (uses environment variables)

#### 🧠 Memory Module (`memory/`)
- **Purpose**: Manages conversation history and memory extraction
- **Key Features**:
  - Maintains conversation history with configurable limits
  - Extracts conversation context for LLM prompts
  - Topic extraction from conversations
  - Conversation summarization

#### 🎭 Personality Module (`personality/`)
- **Purpose**: Manages response tone and AI personality traits
- **Key Features**:
  - Multiple personality tones (friendly, professional, casual, empathetic, enthusiastic)
  - Dynamic tone application to responses
  - Customizable system prompts
  - Runtime personality switching

#### 📊 Data Module (`data/`)
- **Purpose**: Contains sample conversation data
- **Key Features**:
  - Example chat conversations
  - Demonstrates conversation format
  - Can be loaded for testing

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- (Optional) [Ollama](https://ollama.ai/) installed locally for full LLM functionality

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Vinaytandle/guppshupp-ai.git
   cd guppshupp-ai
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):
   Create a `.env` file in the project root for custom configurations:
   ```env
   OLLAMA_BASE_URL=http://localhost:11434
   ```

### Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   Open your browser and navigate to `http://localhost:8501`

### Running with Ollama (Optional)

For full AI functionality, install and run Ollama:

1. **Install Ollama**:
   Follow instructions at [ollama.ai](https://ollama.ai/)

2. **Pull a model**:
   ```bash
   ollama pull llama2
   ```

3. **Ensure Ollama is running**:
   ```bash
   ollama serve
   ```

4. **Run the Streamlit app**:
   The app will automatically detect and connect to Ollama

### Demo Mode

If Ollama is not available, the app runs in demo mode with placeholder responses. You can still:
- Test the UI and conversation flow
- Try different personality tones
- Load and view sample conversations
- Explore memory and context features

## 🎯 Features

- **🎨 Multiple Personality Tones**: Choose from friendly, professional, casual, empathetic, or enthusiastic
- **💭 Conversation Memory**: Maintains context across messages
- **📝 Topic Extraction**: Automatically identifies conversation topics
- **🔄 Sample Data Loading**: Load example conversations to test the app
- **🎛️ Real-time Configuration**: Change settings without restarting
- **🔌 Modular Design**: Easy to extend and customize

## 🛠️ Development

### Project Structure

The project uses a modular structure where each component is independent and can be tested separately:

- **app.py**: Orchestrates all modules and provides the UI
- **llm/**: Handles all LLM-related operations
- **memory/**: Manages conversation state and history
- **personality/**: Controls response tone and style
- **data/**: Stores sample and configuration data

### Configuration

No API keys are hardcoded. Configuration is managed through:
- Environment variables (`.env` file)
- Streamlit session state
- Module initialization parameters

### Extending the Application

To add new features:

1. **Add a new personality tone**: Edit `personality/engine.py` and add to `PersonalityTone` enum
2. **Integrate a different LLM**: Implement a new client in `llm/` following the same interface
3. **Enhance memory**: Extend `ConversationMemory` class with new extraction methods
4. **Add new UI features**: Modify `app.py` following Streamlit conventions

## 📦 Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management

See `requirements.txt` for specific versions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available for educational and demonstration purposes.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- LLM integration powered by [Ollama](https://ollama.ai/)

---

**Note**: This is a minimal demo project designed to showcase architecture and modular design. For production use, consider adding authentication, database persistence, and more robust error handling.