"""Application configuration."""
import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Database
    database_url: str = "postgresql://airi_user:airi_password@localhost:5432/airi_db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Elasticsearch
    elasticsearch_url: str = "http://localhost:9200"
    
    # Vector DB
    vector_db_type: str = "pinecone"  # or 'milvus'
    pinecone_api_key: Optional[str] = None
    pinecone_environment: str = "us-west1-gcp"
    pinecone_index_name: str = "airi-embeddings"
    
    # LLM & Embeddings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # Data Ingestion
    newsapi_key: Optional[str] = None
    newsapi_rate_limit: int = 100
    
    # Email
    sendgrid_api_key: Optional[str] = None
    sendgrid_from_email: str = "noreply@airi.local"
    
    # Security
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    
    # Logging
    log_level: str = "INFO"
    
    # Feature Flags
    enable_rag_summarization: bool = True
    enable_risk_scoring: bool = True
    enable_email_alerts: bool = True
    
    # Environment
    debug: bool = False
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

