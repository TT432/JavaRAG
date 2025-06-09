# JavaRAG - Java Code Knowledge Base System

> **Language / 语言**: [English](README.md) | [中文](README_ZH.md)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![uv](https://img.shields.io/badge/uv-enabled-brightgreen.svg)](https://github.com/astral-sh/uv)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4%2B-FF6B6B.svg)](https://www.trychroma.com/)

A Java code knowledge base system based on Retrieval-Augmented Generation (RAG) technology, specifically designed for parsing, indexing, and querying Java source code. This system can automatically extract Java source code from JAR files, build a code knowledge base using advanced vectorization techniques, and provide intelligent code Q&A services through integration with SiliconFlow API and DeepSeek-V3 model.

## 🎯 Project Overview

### Problems Solved

JavaRAG aims to solve the following common problems in Java development:

1. **Code Understanding Difficulties**: Developers find it hard to quickly understand complex code structures and logic when facing large Java projects
2. **Insufficient API Documentation**: Many open-source Java libraries lack detailed documentation, requiring developers to read source code directly
3. **Low Code Search Efficiency**: Traditional text search cannot understand code semantics, making it difficult to find relevant code snippets
4. **Knowledge Transfer Difficulties**: Code knowledge in projects is hard to effectively transfer to new team members
5. **Low Code Reuse Rate**: Developers find it difficult to discover existing reusable code components in projects

### Core Value

- **Intelligent Code Understanding**: AI-based code semantic understanding, providing accurate code explanations and Q&A
- **Efficient Knowledge Retrieval**: Vectorized search technology for quickly locating relevant code snippets
- **Automated Processing**: Automatically extract and parse Java source code from JAR files
- **Diverse Interfaces**: Provide CLI, Web UI, and REST API multiple usage methods
- **Extensible Architecture**: Modular design, easy to extend and customize

## ✨ Key Features

- 🔍 **Intelligent Code Parsing**: Automatically parse Java source code in JAR files
- 🧠 **Vectorized Storage**: Build efficient code vector database using ChromaDB
- 💬 **Intelligent Q&A**: Java code Q&A system based on RAG technology
- 🚀 **SiliconFlow Integration**: Integrate DeepSeek-V3 model for powerful code understanding capabilities
- 🌐 **Web API**: Provide RESTful API interface
- 🖥️ **Command Line Tool**: Support command line operations
- 🎨 **Web Interface**: Modern Web UI interface

## 📁 Project Structure

```
javarag/
├── .AddCompLib/                 # AddCompLib configuration
├── .env                         # Environment variables configuration
├── .env.example                 # Environment variables example
├── .gitignore                   # Git ignore file configuration
├── .venv/                       # Python virtual environment
├── README.md                    # Project README file
├── README_ZH.md                 # Chinese README file
├── TODO.md                      # TODO list
├── chroma_db/                   # ChromaDB data directory
├── pyproject.toml               # Project configuration (PEP 518)
├── src/                         # Core source code
│   ├── __init__.py              # Package initialization file
│   ├── config.py                # Configuration management
│   ├── demo.py                  # Demo script
│   ├── frontend/                # Web frontend interface
│   │   ├── index.html           # Main page
│   │   ├── webui_server.py      # WebUI server
│   │   └── static/              # Static resources (CSS, JS, etc.)
│   ├── ingestion_pipeline.py    # Data ingestion pipeline
│   ├── jar_processor.py         # JAR file processor
│   ├── java_parser.py           # Java code parser
│   ├── rag_service.py           # RAG service core
│   ├── sources/                 # JAR file storage directory
│   ├── temp/                    # Temporary file directory
│   └── vector_db.py             # Vector database operations
├── uv.lock                      # uv dependency lock file
└── webui.py                     # WebUI startup script
```

## 🚀 Quick Start

### Environment Requirements

- **Python**: 3.10+ (recommended 3.11 or 3.12)
- **Package Manager**: uv (recommended) or pip
- **API Key**: SiliconFlow API key (for AI Q&A functionality)
- **System Requirements**: 
  - Memory: Minimum 4GB RAM (recommended 8GB+)
  - Storage: At least 2GB available space
  - Network: Stable internet connection (for downloading models and API calls)

### Installation Steps

#### Method 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that can significantly improve dependency installation speed.

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac
# Or use PowerShell on Windows:
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Clone the project
git clone <repository-url>
cd javarag

# 3. Create virtual environment and install dependencies
uv sync

# 4. Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

#### Method 2: Using pip

```bash
# 1. Clone the project
git clone <repository-url>
cd javarag

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# 4. Upgrade pip and install dependencies
pip install --upgrade pip
pip install .
```

### Configuration

1. Copy environment variables example file:
```bash
cp .env.example .env
```

2. Edit `.env` file to configure SiliconFlow API:
```env
# SiliconFlow API configuration
OPENAI_API_KEY=your_siliconflow_api_key
OPENAI_API_BASE=https://api.siliconflow.cn/v1
OPENAI_MODEL=deepseek-ai/DeepSeek-V3

# ChromaDB configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db

# API server configuration
API_HOST=0.0.0.0
API_PORT=8000

# WebUI configuration
WEBUI_HOST=0.0.0.0
WEBUI_PORT=8847

# LLM configuration
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000

# Embedding model configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Data Ingestion

Place JAR files in the `src/sources/` directory, then run the data ingestion pipeline:

```bash
# Using uv
uv run python src/ingestion_pipeline.py --jar-path src/sources

# Using python
python src/ingestion_pipeline.py --jar-path src/sources
```

## 📖 Usage Methods

### Web User Interface (WebUI)

#### Starting WebUI Server

```bash
# Start with default configuration
python webui.py

# Specify port and host
python webui.py --host 0.0.0.0 --port 9000

# Start in development mode (auto-reload)
python webui.py --reload

# Run with uv
uv run python webui.py --verbose
```

#### WebUI Features

After accessing `http://localhost:8847`, you can use the following features:

- **📁 File Management**:
  - Drag and drop JAR file uploads
  - View indexed file list
  - Delete unnecessary files
  - Re-index files

- **💬 Intelligent Q&A**:
  - Natural language queries for Java code
  - View AI-generated detailed answers
  - View related source code snippets
  - Copy code to clipboard

- **🔍 Code Search**:
  - Semantic search for code snippets
  - Exact matching of class and method names
  - Filter results by file type
  - Highlight matching content

### Python Programming Interface

#### Basic Usage

```python
from src.rag_service import RAGService
from src.vector_db import VectorDatabase
from src.ingestion_pipeline import IngestionPipeline

# Initialize RAG service
rag = RAGService(collection_name="java_code_chunks")

# Query code
result = rag.query(
    query="What is Spring Boot auto-configuration?",
    top_k=5,
    include_sources=True
)

print(f"Answer: {result['answer']}")
print(f"Related source code: {len(result['sources'])} snippets")
```

#### Advanced Usage

```python
# Custom configuration
from src.config import settings

# Modify configuration
settings.llm_temperature = 0.2
settings.llm_max_tokens = 2000

# Initialize data ingestion pipeline
pipeline = IngestionPipeline()

# Process JAR file
result = pipeline.ingest_jar_file(
    jar_path="path/to/your-sources.jar",
    reset_collection=False
)

if result["success"]:
    print(f"Successfully processed {result['chunks_processed']} code blocks")
else:
    print(f"Processing failed: {result['error']}")

# Direct vector database operations
vector_db = VectorDatabase("custom_collection")

# Search similar code
similar_chunks = vector_db.search(
    query="dependency injection",
    top_k=10,
    filter_metadata={"file_type": "java"}
)

for chunk in similar_chunks:
    print(f"File: {chunk['source_file']}")
    print(f"Similarity: {chunk['similarity']:.3f}")
    print(f"Code: {chunk['content'][:200]}...")
    print("-" * 50)
```

## 🛠️ Technology Stack & Dependencies

### Core Technology Stack

| Technology Component | Version Requirement | Purpose |
|---------------------|---------------------|----------|
| **Python** | 3.10+ | Main programming language |
| **FastAPI** | 0.104+ | Web API framework, providing high-performance REST API services |
| **Uvicorn** | 0.24+ | ASGI server for running FastAPI applications |
| **ChromaDB** | 0.4.22+ | Vector database for storing and retrieving code embedding vectors |
| **LangChain** | 0.1.0+ | LLM application development framework, providing RAG functionality |
| **Sentence Transformers** | 2.2.2+ | Text embedding model for converting code to vectors |
| **Tree-sitter** | 0.20.4+ | Code parser for parsing Java syntax trees |

### AI and Machine Learning Libraries

| Library Name | Version | Function Description |
|-------------|---------|---------------------|
| **langchain-openai** | 0.0.5+ | OpenAI-compatible LLM interface |
| **langchain-community** | 0.0.20+ | LangChain community extensions |
| **sentence-transformers** | 2.2.2+ | Pre-trained sentence embedding models |
| **numpy** | 1.24.0+ | Numerical computing library |
| **pandas** | 2.0.0+ | Data processing and analysis |

### Web Development and API Libraries

| Library Name | Version | Function Description |
|-------------|---------|---------------------|
| **fastapi** | 0.104.1+ | Modern Web API framework |
| **uvicorn** | 0.24.0+ | High-performance ASGI server |
| **python-multipart** | 0.0.6+ | File upload support |
| **aiofiles** | 23.2.1+ | Asynchronous file operations |
| **httpx** | 0.25.0+ | Asynchronous HTTP client |

### Configuration and Tool Libraries

| Library Name | Version | Function Description |
|-------------|---------|---------------------|
| **pydantic** | 2.5.0+ | Data validation and settings management |
| **pydantic-settings** | 2.1.0+ | Configuration management |
| **python-dotenv** | 1.0.0+ | Environment variable management |
| **click** | 8.1.7+ | Command line interface framework |
| **rich** | 13.7.0+ | Terminal beautification and progress bars |
| **tqdm** | 4.66.1+ | Progress bar display |

### Development and Testing Tools

| Library Name | Version | Function Description |
|-------------|---------|---------------------|
| **pytest** | 7.4.0+ | Unit testing framework |
| **pytest-asyncio** | 0.21.0+ | Asynchronous testing support |
| **black** | 23.0.0+ | Code formatting tool |
| **flake8** | 6.0.0+ | Code style checking |
| **mypy** | 1.5.0+ | Static type checking |

## 🗄️ Database Architecture

### ChromaDB Vector Database

JavaRAG uses ChromaDB as the vector database for storing and retrieving Java code embedding vectors.

#### Database Configuration

```python
# Database settings
CHROMA_PERSIST_DIRECTORY = "./chroma_db"  # Data persistence directory
COLLECTION_NAME = "java_code_chunks"     # Default collection name
EMBEDDING_MODEL = "all-MiniLM-L6-v2"    # Embedding model
```

#### Data Structure

Each code block stores the following information in the database:

```python
{
    "id": "unique_chunk_id",           # Unique identifier
    "content": "Java code content",     # Code text
    "embedding": [0.1, 0.2, ...],      # 384-dimensional vector
    "metadata": {
        "source_file": "com/example/MyClass.java",
        "class_name": "MyClass",
        "method_name": "myMethod",
        "start_line": 10,
        "end_line": 25,
        "chunk_type": "method",        # method, class, interface, field
        "file_type": "java",
        "jar_source": "spring-core-6.0.0-sources.jar",
        "package_name": "com.example",
        "access_modifier": "public",
        "is_static": false,
        "is_abstract": false,
        "annotations": ["@Override", "@Deprecated"]
    }
}
```

#### Indexing Strategy

1. **Semantic Indexing**: Use sentence-transformers model to generate semantic embeddings of code
2. **Metadata Indexing**: Filter based on metadata such as class names, method names, package names
3. **Hybrid Retrieval**: Combine semantic similarity and metadata matching

#### Query Optimization

```python
# Query example
similar_chunks = vector_db.search(
    query="Spring dependency injection",
    top_k=10,
    filter_metadata={
        "chunk_type": "method",
        "package_name": "org.springframework"
    },
    similarity_threshold=0.7
)
```

### Data Persistence

- **Storage Location**: `./chroma_db/` directory
- **Backup Strategy**: Support database export and import
- **Version Control**: Support collection version management
- **Data Migration**: Provide data migration tools

## 🧪 Testing

### Testing Framework

The project uses pytest as the main testing framework, supporting unit tests, integration tests, and end-to-end tests.

### Running Tests

#### Unit Tests
```bash
# Run all unit tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_vector_db.py -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

#### Integration Tests
```bash
# Test SiliconFlow API connection
uv run python tests_integration/test_siliconflow.py

# System integration tests
uv run python tests_integration/test_system.py

# End-to-end tests
uv run pytest tests_integration/ -v
```

#### Performance Tests
```bash
# Vector database performance tests
uv run python tests/test_performance.py

# API response time tests
uv run python tests_integration/test_api_performance.py
```

### Test Coverage

Target test coverage:
- Core modules: >90%
- API interfaces: >85%
- Utility functions: >80%

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Docker

```bash
# Build image
docker build -t javarag .

# Run container
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key \
  -e OPENAI_BASE_URL=https://api.siliconflow.cn/v1 \
  -v $(pwd)/sources:/app/sources \
  -v $(pwd)/chroma_db:/app/chroma_db \
  javarag
```

## 📚 API Documentation

After starting the API server, visit the following addresses to view API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main API Endpoints

- `POST /query` - Query Java code
- `GET /health` - Health check
- `GET /stats` - System statistics

## ⚙️ Configuration Instructions

### Environment Variables

| Variable Name | Description | Default Value |
|--------------|-------------|---------------|
| `OPENAI_API_KEY` | SiliconFlow API key | Required |
| `OPENAI_BASE_URL` | API base URL | `https://api.siliconflow.cn/v1` |
| `OPENAI_MODEL` | Model to use | `deepseek-ai/DeepSeek-V3` |
| `CHROMA_DB_PATH` | ChromaDB data path | `./chroma_db` |
| `COLLECTION_NAME` | Collection name | `java_code_chunks` |
| `CHUNK_SIZE` | Code chunk size | `1000` |
| `CHUNK_OVERLAP` | Code chunk overlap | `200` |
| `TOP_K` | Number of retrieval results | `5` |

### Supported Models

SiliconFlow platform supports multiple open-source models:
- DeepSeek series: `deepseek-ai/DeepSeek-V3`, `deepseek-ai/DeepSeek-R1`
- Qwen series: `Qwen/Qwen2.5-72B-Instruct`, `Qwen/Qwen2.5-Coder-32B-Instruct`
- GLM series: `THUDM/glm-4-9b-chat`

## 🔧 Development Guide

### Code Standards and Best Practices

#### Code Style

- **Formatting**: Use `black` for code formatting
- **Import Sorting**: Use `isort` for sorting import statements
- **Type Checking**: Use `mypy` for static type checking
- **Code Checking**: Use `flake8` for code style checking

```bash
# Code formatting
uv run black src/ tests/

# Import sorting
uv run isort src/ tests/

# Type checking
uv run mypy src/

# Code checking
uv run flake8 src/ tests/
```

#### Testing Standards

```python
# Test file naming: test_*.py
# Test class naming: Test*
# Test method naming: test_*

class TestRAGService:
    """RAG service test class."""
    
    def test_query_with_valid_input(self):
        """Test query functionality with valid input."""
        rag = RAGService()
        result = rag.query("test query")
        assert "answer" in result
        assert isinstance(result["sources"], list)
```

#### Documentation Standards

```python
def complex_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """Complex function documentation example.
    
    This function demonstrates how to write standard docstrings.
    
    Args:
        param1: Description of the first parameter
        param2: Description of the second parameter, default value is 10
        
    Returns:
        Dictionary containing results, format as follows:
        {
            "status": "success",
            "data": [...]
        }
        
    Raises:
        ValueError: Raised when param1 is empty
        TypeError: Raised when param2 is not an integer
        
    Example:
        >>> result = complex_function("test", 20)
        >>> print(result["status"])
        success
    """
    pass
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SiliconFlow](https://siliconflow.cn/) - Providing powerful AI model APIs
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [LangChain](https://langchain.com/) - LLM application development framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

---

**JavaRAG** - Making Java code knowledge accessible 🚀