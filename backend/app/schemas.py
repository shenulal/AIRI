"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


# Company Schemas
class CompanyBase(BaseModel):
    """Base company schema."""
    name: str
    ticker: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Schema for creating a company."""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating a company."""
    name: Optional[str] = None
    ticker: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class CompanyResponse(CompanyBase):
    """Schema for company response."""
    id: str
    risk_score: float
    executive_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CompanyProfileResponse(CompanyResponse):
    """Detailed company profile with recent documents."""
    recent_documents: List['DocumentResponse'] = []
    sentiment_trend: Optional[Dict[str, Any]] = None
    risk_score_history: List[Dict[str, Any]] = []


# Document Schemas
class DocumentBase(BaseModel):
    """Base document schema."""
    title: str
    content: str
    source: str
    source_url: Optional[str] = None
    published_at: Optional[datetime] = None


class DocumentCreate(DocumentBase):
    """Schema for creating a document."""
    company_id: str


class DocumentResponse(DocumentBase):
    """Schema for document response."""
    id: str
    company_id: str
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    ingested_at: datetime
    
    class Config:
        from_attributes = True


# Risk Score Schemas
class RiskScoreResponse(BaseModel):
    """Schema for risk score response."""
    company_id: str
    score: float
    rule_score: Optional[float] = None
    ml_score: Optional[float] = None
    features: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Watchlist Schemas
class WatchlistItemResponse(BaseModel):
    """Schema for watchlist item."""
    id: str
    company_id: str
    added_at: datetime
    
    class Config:
        from_attributes = True


class WatchlistBase(BaseModel):
    """Base watchlist schema."""
    name: str
    description: Optional[str] = None


class WatchlistCreate(WatchlistBase):
    """Schema for creating a watchlist."""
    pass


class WatchlistResponse(WatchlistBase):
    """Schema for watchlist response."""
    id: str
    user_id: str
    items: List[WatchlistItemResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WatchlistAddCompanyRequest(BaseModel):
    """Schema for adding company to watchlist."""
    company_id: str


# Alert Schemas
class AlertBase(BaseModel):
    """Base alert schema."""
    email: str
    alert_type: str
    threshold: Optional[float] = None


class AlertCreate(AlertBase):
    """Schema for creating an alert."""
    watchlist_id: Optional[str] = None


class AlertResponse(AlertBase):
    """Schema for alert response."""
    id: str
    user_id: str
    watchlist_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    last_triggered_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Search Schemas
class SearchRequest(BaseModel):
    """Schema for search request."""
    query: str
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)


class SearchResponse(BaseModel):
    """Schema for search response."""
    total: int
    results: List[CompanyResponse]
    query: str


# Health Check
class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    timestamp: datetime
    version: str = "0.1.0"


# Update forward references
CompanyProfileResponse.model_rebuild()

