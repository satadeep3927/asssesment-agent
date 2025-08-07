# 🎯 AI Assessment Generator

A comprehensive Streamlit application that leverages AI to generate educational assessments with customizable parameters, question types, and difficulty levels.

## ✨ Features

- **Intelligent Assessment Generation**: Create assessments based on curriculum standards and learning objectives
- **Bloom's Taxonomy Integration**: Target specific cognitive levels (Remember, Understand, Apply, Analyze, Evaluate, Create)
- **Flexible Question Types**: Support for Multiple Choice, Short Answer, and Long Answer questions
- **Customizable Distribution**: Control the percentage of each question type
- **Comprehensive Answer Keys**: Include explanations, marking criteria, and key points
- **Assessment Analytics**: View difficulty distribution and question type statistics
- **Export Capabilities**: Download assessments in JSON or text format
- **Assessment History**: Track and revisit previously generated assessments

## 🏗️ Architecture

The application follows a modular architecture:

```
assessment-agent/
├── agents/
│   └── assementagent.py      # Main assessment agent
├── common/
│   └── config.py             # Configuration management
├── prompts/
│   └── assesment.j2          # Jinja2 prompt template
├── schema/
│   └── schema.py             # Pydantic data models
├── services/
│   ├── llmmanager.py         # LLM interaction service
│   └── promptmanager.py      # Prompt management service
├── test/
│   └── test_llmmanager.py    # Test files
├── app.py                    # Streamlit application
├── requirements.txt          # Python dependencies
└── streamlit_ui.py          # UI components
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- API key for your chosen LLM provider (OpenAI, Claude, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assessment-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your LLM settings**
   
   Update `common/config.py` with your API credentials:
   ```python
   LLM_API_KEY = "your-api-key"
   LLM_API = "your-api-endpoint" 
   LLM_MODEL = "your-model-name"
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### Generating an Assessment

1. **Configure Assessment Parameters**
   - Enter curriculum standard (e.g., "CBSE Class 10", "Common Core Grade 8")
   - Define learning objectives
   - Select Bloom's taxonomy level
   - Choose difficulty level
   - Set total marks and number of questions

2. **Customize Question Distribution**
   - Adjust percentages for MCQ, Short Answer, and Long Answer questions
   - Ensure percentages sum to 1.0

3. **Add Additional Requirements** (Optional)
   - Include specific instructions or constraints
   - Request focus areas or special considerations

4. **Generate Assessment**
   - Click "Generate Assessment" 
   - Wait for AI processing (may take 30-60 seconds)
   - Review the generated assessment

### Viewing Assessment Results

The generated assessment includes:

- **Question Details**: Question text, type, marks allocation
- **Multiple Choice Options**: With correct answer indicators
- **Comprehensive Answer Keys**: Explanations and marking criteria
- **Assessment Statistics**: Difficulty and type distribution charts
- **Export Options**: Download as JSON or formatted text

### Assessment History

- View all previously generated assessments
- Quick access to assessment details
- Timestamp tracking for organizational purposes

## 🔧 Configuration

### LLM Provider Setup

The application supports various LLM providers. Configure in `common/config.py`:

**OpenAI:**
```python
LLM_API = "https://api.openai.com/v1"
LLM_MODEL = "gpt-4"
LLM_API_KEY = "sk-your-openai-key"
```

**Claude:**
```python
LLM_API = "https://api.anthropic.com"
LLM_MODEL = "claude-3-sonnet-20240229"
LLM_API_KEY = "your-anthropic-key"
```

### Prompt Customization

Modify `prompts/assesment.j2` to customize the AI prompt template:

- Adjust assessment generation instructions
- Add specific requirements or constraints
- Modify output format specifications

## 📊 Data Models

### AssessmentRequest
- Curriculum standard and learning objectives
- Bloom's taxonomy and difficulty levels
- Question count and mark distribution
- Question type percentages

### AssessmentResult
- Generated questions with answer keys
- Assessment metadata and statistics
- Student instructions and teacher notes

### Question Types
- **Multiple Choice**: 4 options with single correct answer
- **Short Answer**: 2-5 marks, concise responses
- **Long Answer**: 5+ marks, detailed analysis required

## 🧪 Testing

Run tests to ensure system functionality:

```bash
python -m pytest test/
```

For manual testing:
```bash
python test/test_llmmanager.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

1. Check the [Issues](../../issues) page for common problems
2. Create a new issue with detailed description
3. Include error messages and system information

## 🔮 Roadmap

- [ ] Support for additional question types (True/False, Fill-in-the-blank)
- [ ] Integration with Learning Management Systems (LMS)
- [ ] Advanced assessment analytics and insights
- [ ] Collaborative assessment creation
- [ ] Question bank management
- [ ] Auto-grading capabilities
- [ ] Multi-language support

## 📚 Documentation

- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [Deployment Guide](docs/deployment.md)

---

**Built with ❤️ using Streamlit, Pydantic, and AI**
