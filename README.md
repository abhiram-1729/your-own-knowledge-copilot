# 🧠 Personal Knowledge Copilot

<div align="center">

![Knowledge Copilot Logo](https://img.shields.io/badge/🧠-Knowledge%20Copilot-blue?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**AI-powered document intelligence system** that transforms your personal documents into an interactive knowledge base with advanced RAG (Retrieval-Augmented Generation) capabilities.

[▶️ **Live Demo**](#deployment) • [📖 **Documentation**](#documentation) • [🚀 **Quick Start**](#quick-start) • [🤖 **API Reference**](#api-endpoints)

</div>

---

## 🌟 Overview

Personal Knowledge Copilot is a sophisticated full-stack application that allows you to upload documents (PDF, DOCX, TXT, MD, EML, HTML) and interact with them through an intelligent AI chat interface. Built with modern technologies and featuring a beautiful, responsive UI, it provides instant answers based strictly on your uploaded content.

### 🎯 Key Features

- 📄 **Multi-format Document Support** - PDF, DOCX, TXT, Markdown, EML, HTML
- 🤖 **AI-Powered Q&A** - Smart responses using Gemini AI with fallback mechanisms
- 🔍 **Intelligent Search** - Advanced vector similarity search with ChromaDB
- 🎨 **Modern UI/UX** - Beautiful glassmorphism design with smooth animations
- 📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile
- 🔄 **Real-time Processing** - Instant document processing and chat responses
- 📊 **Source Citations** - Transparent source references for all answers
- 🗑️ **Document Management** - Easy upload, view, and delete functionality

---

## 🚀 Deployment

### 🌐 Live Application

> **🔗 Live Demo**: `[Your Deployed Application Link Here]`
> 
> *Placeholder for your deployed application URL*

### 📋 Deployment Checklist

- [ ] Frontend deployed (Vercel/Netlify/Render)
- [ ] Backend deployed (Render/Railway/Heroku)
- [ ] Environment variables configured
- [ ] Database persistence enabled
- [ ] SSL certificates active
- [ ] Custom domain configured (optional)

### 🐳 Docker Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/personal-knowledge-copilot.git
cd personal-knowledge-copilot

# Build and run with Docker Compose
docker-compose up -d
```

---

## 📖 Documentation

### 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │    │   FastAPI       │    │   ChromaDB      │
│   (Frontend)    │◄──►│   Backend       │◄──►│   Vector Store  │
│                 │    │                 │    │                 │
│ • Modern UI     │    │ • Document API  │    │ • Embeddings    │
│ • Real-time     │    │ • Query API     │    │ • Similarity    │
│ • Animations    │    │ • RAG Pipeline  │    │ • Storage       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Framer Motion │    │   Gemini AI     │    │   SQLite DB     │
│   Toast Notif.  │    │   LLM Service   │    │   Metadata      │
│   Lucide Icons  │    │   Fallback      │    │   File Info     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🛠️ Tech Stack

#### Frontend
- **React 18** - Modern UI framework
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Hot Toast** - Elegant notifications
- **Lucide React** - Professional icon library
- **Axios** - HTTP client

#### Backend
- **FastAPI** - High-performance async framework
- **Python 3.11** - Modern Python features
- **ChromaDB** - Vector database for embeddings
- **Sentence Transformers** - Text embeddings
- **Google Generative AI** - Gemini AI integration
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation

#### Infrastructure
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Python-dotenv** - Environment management

---

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.11+** - Backend development
- **Node.js 18+** - Frontend development
- **Git** - Version control

### 🔧 Installation

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/personal-knowledge-copilot.git
cd personal-knowledge-copilot
```

#### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your Gemini API key:
# GEMINI_API_KEY=your_gemini_api_key_here
```

#### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Copy environment file (if needed)
cp .env.example .env.local
```

#### 4. Start Development Servers

**Backend (Terminal 1):**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```
*Backend runs on: http://localhost:8000*

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```
*Frontend runs on: http://localhost:3000*

### 🗝️ Environment Variables

Create a `.env` file in the backend directory:

```env
# Gemini AI API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration (Optional)
DATABASE_URL=sqlite:///./knowledge_copilot.db

# ChromaDB Settings (Optional)
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### 🎯 First Run

1. **Access the Application**: Open http://localhost:3000
2. **Upload Documents**: Drag & drop or click to upload files
3. **Ask Questions**: Type questions about your documents
4. **Get AI Responses**: Receive intelligent answers with sources

---

## 🤖 API Endpoints

### 📄 Document Management

#### Upload Document
```http
POST /api/upload
Content-Type: multipart/form-data

# Response
{
  "message": "Document uploaded successfully",
  "document_id": "uuid",
  "chunks_processed": 42
}
```

#### Get All Documents
```http
GET /api/documents

# Response
[
  {
    "id": "uuid",
    "filename": "document.pdf",
    "file_type": "application/pdf",
    "upload_date": "2024-01-01T00:00:00",
    "processed": true
  }
]
```

#### Delete Document
```http
DELETE /api/documents/{document_id}

# Response
{
  "message": "Document deleted successfully"
}
```

### 💬 Chat & Query

#### Ask Question
```http
POST /api/query
Content-Type: application/json

{
  "question": "What are the main concepts in this document?"
}

# Response
{
  "answer": "Based on your documents...",
  "sources": [
    {
      "filename": "document.pdf",
      "content_preview": "..."
    }
  ],
  "conversation_id": "uuid"
}
```

### 🏥 Health Check

#### System Status
```http
GET /

# Response
{
  "message": "Personal Knowledge Copilot API is running"
}
```

---

## 🎨 Features & Functionality

### 📄 Document Processing

- **Supported Formats**: PDF, DOCX, TXT, MD, EML, HTML
- **Text Extraction**: Advanced content extraction from various file types
- **Chunking Strategy**: Intelligent text segmentation for optimal search
- **Vector Embeddings**: High-quality text representations
- **Metadata Storage**: Complete file information tracking

### 🔍 Search & Retrieval

- **Semantic Search**: Vector similarity matching
- **Context Ranking**: Relevance-based document ordering
- **Source Attribution**: Transparent answer sourcing
- **Multi-document Queries**: Cross-document information synthesis

### 🤖 AI Integration

- **Gemini AI**: Primary LLM for intelligent responses
- **Smart Fallback**: Graceful degradation when AI unavailable
- **Context-Aware**: Conversation history integration
- **Document-Only Responses**: Strict adherence to uploaded content
- **Structured Output**: Formatted, readable responses

### 🎨 User Interface

- **Modern Design**: Glassmorphism with gradient accents
- **Smooth Animations**: Framer Motion powered transitions
- **Responsive Layout**: Mobile-first design approach
- **Interactive Elements**: Hover states and micro-interactions
- **Toast Notifications**: Non-intrusive user feedback
- **Drag & Drop**: Intuitive file upload experience

---

## 🔧 Configuration

### 🧠 AI Model Settings

```python
# In backend/app/agent.py
GENERATION_CONFIG = {
    "temperature": 0.3,    # Creativity level
    "top_p": 0.8,         # Nucleus sampling
    "top_k": 40,          # Token diversity
    "max_output_tokens": 1000  # Response length
}
```

### 📊 Vector Store Settings

```python
# In backend/app/vector_store.py
VECTOR_CONFIG = {
    "collection_name": "documents",
    "embedding_model": "all-MiniLM-L6-v2",
    "chunk_size": 1000,
    "chunk_overlap": 200
}
```

### 🎨 UI Customization

```javascript
// In frontend/src/components/Dashboard.jsx
const UI_CONFIG = {
  "primary_color": "from-blue-500 to-purple-600",
  "animation_duration": "300ms",
  "max_file_size": "50MB",
  "supported_formats": [".pdf", ".docx", ".txt", ".md", ".eml", ".html"]
}
```

---

## 🧪 Testing

### 🔄 Running Tests

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### 📊 Test Coverage

- **Unit Tests**: Core functionality validation
- **Integration Tests**: API endpoint testing
- **E2E Tests**: Complete user workflows
- **Performance Tests**: Load and stress testing

---

## 📚 Development Guide

### 🏗️ Project Structure

```
personal-knowledge-copilot/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── agent.py        # AI chat logic
│   │   ├── database.py     # Database models
│   │   ├── document_processor.py  # File processing
│   │   └── vector_store.py # Vector database
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── Dashboard.jsx  # Main UI component
│   │   ├── contexts/
│   │   └── App.jsx        # React application
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
├── README.md              # This file
└── docker-compose.yml     # Docker configuration
```

### 🔧 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 📝 Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **Components**: Keep components small and focused
- **Comments**: Document complex logic
- **Testing**: Maintain >80% code coverage

---

## 🚀 Deployment Guide

### 🌐 Production Deployment

#### Frontend (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod
```

#### Backend (Render)
```bash
# Create render.yaml
cd backend
# Deploy via Render dashboard
```

#### Database Setup
```bash
# Configure persistent storage
# Set up ChromaDB persistence
# Configure SQLite backups
```

### 🔒 Security Considerations

- **API Keys**: Never expose in client-side code
- **File Uploads**: Validate file types and sizes
- **Rate Limiting**: Implement API rate limits
- **CORS**: Configure proper origins
- **Authentication**: Add user authentication (future)

---

## 🐛 Troubleshooting

### 🔧 Common Issues

#### Backend Issues
```bash
# Port already in use
lsof -ti:8000 | xargs kill

# Python version mismatch
python --version  # Should be 3.11+
```

#### Frontend Issues
```bash
# Clear cache
npm run build -- --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### Database Issues
```bash
# Reset ChromaDB
rm -rf ./chroma_db

# Clear SQLite
rm knowledge_copilot.db
```

### 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/personal-knowledge-copilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/personal-knowledge-copilot/discussions)
- **Email**: your.email@example.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google AI** - For Gemini API access
- **ChromaDB** - Vector database functionality
- **Sentence Transformers** - Text embedding models
- **FastAPI** - Modern Python web framework
- **React** - User interface library
- **Tailwind CSS** - Utility-first CSS framework

---

## 📈 Roadmap

### 🚀 Upcoming Features

- [ ] **User Authentication** - Multi-user support
- [ ] **Document Sharing** - Collaborative knowledge bases
- [ ] **Advanced Search** - Filters and advanced queries
- [ ] **Export Features** - PDF/Markdown export
- [ ] **Mobile App** - React Native application
- [ ] **API Rate Limiting** - Usage controls
- [ ] **Analytics Dashboard** - Usage insights
- [ ] **Plugin System** - Extensible architecture

### 🎯 Version History

- **v2.0.0** - Enhanced UI with modern design
- **v1.5.0** - Gemini AI integration
- **v1.0.0** - Initial release with core functionality

---

<div align="center">

**⭐ Star this repository** if it helped you build something amazing!

[🔝 Back to Top](#-personal-knowledge-copilot)

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>