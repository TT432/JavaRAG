"""Configuration module for Java RAG Knowledge Base."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Compatible API Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.siliconflow.cn/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "deepseek-ai/DeepSeek-V3")
    
    # ChromaDB Configuration
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Embedding Model Configuration
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # WebUI Configuration
    webui_host: str = os.getenv("WEBUI_HOST", "0.0.0.0")
    webui_port: int = int(os.getenv("WEBUI_PORT", "8847"))
    
    # LLM Configuration
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1000"))
    
    # Project paths
    project_root: Path = Path(__file__).parent
    sources_dir: Path = project_root / "sources"
    temp_dir: Path = project_root / "temp"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Ensure required directories exist
settings.sources_dir.mkdir(exist_ok=True)
settings.temp_dir.mkdir(exist_ok=True)
Path(settings.chroma_persist_directory).mkdir(exist_ok=True)