"""
Production-level configuration management
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Environment
    env: str = os.getenv("ENV", "development")
    port: int = int(os.getenv("PORT", 8000))
    
    # Application
    app_name: str = "ICICI Insurance Chatbot"
    app_version: str = "1.0.0"
    debug: bool = env == "development"
    
    # PDF and Web Scraping
    max_pdf_chunks: int = int(os.getenv("MAX_PDF_CHUNKS", 150))
    max_web_pages: int = int(os.getenv("MAX_WEB_PAGES", 10))
    use_web_content: bool = os.getenv("USE_WEB_CONTENT", "true").lower() == "true"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    allowed_origins: List[str] = os.getenv(
        "ALLOWED_ORIGINS", 
        "*" if env == "development" else ""
    ).split(",")
    
    # Rate Limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", 20))
    rate_limit_per_hour: int = int(os.getenv("RATE_LIMIT_PER_HOUR", 200))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "app.log")
    
    # Database
    database_path: str = os.getenv("DATABASE_PATH", "conversations.db")
    embeddings_path: str = os.getenv("EMBEDDINGS_PATH", "embeddings.pkl")
    chunks_path: str = os.getenv("CHUNKS_PATH", "chunks.pkl")
    
    # Model Settings
    model_name: str = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", 0.3))
    top_k_chunks: int = int(os.getenv("TOP_K_CHUNKS", 5))
    
    # Session Settings
    session_timeout_days: int = int(os.getenv("SESSION_TIMEOUT_DAYS", 30))
    max_conversation_history: int = int(os.getenv("MAX_CONVERSATION_HISTORY", 10))
    
    class Config:
        case_sensitive = False

# Global settings instance
settings = Settings()
