"""SQLAlchemy database models."""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, String, Integer, Float, Text, DateTime, Boolean, 
    ForeignKey, JSON, Index, UniqueConstraint, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Company(Base):
    """Canonical company record."""
    __tablename__ = "companies"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    ticker = Column(String(10), unique=True, nullable=True, index=True)
    industry = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Risk & Summary
    risk_score = Column(Float, default=0.0)
    risk_score_updated_at = Column(DateTime, default=datetime.utcnow)
    executive_summary = Column(Text, nullable=True)
    summary_updated_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="company", cascade="all, delete-orphan")
    watchlist_items = relationship("WatchlistItem", back_populates="company", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_company_name", "name"),
        Index("idx_company_ticker", "ticker"),
    )


class Document(Base):
    """Raw ingested documents (news, filings, etc.)."""
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    
    # Content
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(50), nullable=False)  # 'newsapi', 'opencorporates', etc.
    source_url = Column(String(500), nullable=True)
    
    # NLP Results
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    sentiment_label = Column(String(20), nullable=True)  # 'positive', 'negative', 'neutral'
    entities = Column(JSON, nullable=True)  # NER results
    
    # Embeddings
    embedding_id = Column(String(100), nullable=True)  # Reference to vector DB
    
    # Metadata
    published_at = Column(DateTime, nullable=True)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="documents")
    
    __table_args__ = (
        Index("idx_document_company", "company_id"),
        Index("idx_document_source", "source"),
        Index("idx_document_published", "published_at"),
    )


class RiskScore(Base):
    """Historical risk scores for time-series analysis."""
    __tablename__ = "risk_scores"
    
    id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    
    score = Column(Float, nullable=False)
    rule_score = Column(Float, nullable=True)  # Rule-based component
    ml_score = Column(Float, nullable=True)    # ML-based component
    
    # Feature breakdown
    features = Column(JSON, nullable=True)  # Feature values used in scoring
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_risk_score_company", "company_id"),
        Index("idx_risk_score_created", "created_at"),
    )


class Watchlist(Base):
    """User watchlists."""
    __tablename__ = "watchlists"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_watchlist_user", "user_id"),
    )


class WatchlistItem(Base):
    """Companies in a watchlist."""
    __tablename__ = "watchlist_items"
    
    id = Column(String(36), primary_key=True)
    watchlist_id = Column(String(36), ForeignKey("watchlists.id"), nullable=False, index=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    watchlist = relationship("Watchlist", back_populates="items")
    company = relationship("Company", back_populates="watchlist_items")
    
    __table_args__ = (
        UniqueConstraint("watchlist_id", "company_id", name="uq_watchlist_company"),
        Index("idx_watchlist_item_watchlist", "watchlist_id"),
        Index("idx_watchlist_item_company", "company_id"),
    )


class Alert(Base):
    """Alert subscriptions and history."""
    __tablename__ = "alerts"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    watchlist_id = Column(String(36), ForeignKey("watchlists.id"), nullable=True)
    
    email = Column(String(255), nullable=False)
    alert_type = Column(String(50), nullable=False)  # 'risk_increase', 'news', 'sentiment'
    threshold = Column(Float, nullable=True)  # For risk alerts
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_triggered_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index("idx_alert_user", "user_id"),
        Index("idx_alert_watchlist", "watchlist_id"),
    )


class SentimentTimeSeries(Base):
    """Aggregated sentiment over time for each company."""
    __tablename__ = "sentiment_timeseries"
    
    id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    
    date = Column(DateTime, nullable=False)
    avg_sentiment = Column(Float, nullable=False)
    document_count = Column(Integer, default=0)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    
    __table_args__ = (
        UniqueConstraint("company_id", "date", name="uq_sentiment_company_date"),
        Index("idx_sentiment_company", "company_id"),
        Index("idx_sentiment_date", "date"),
    )

