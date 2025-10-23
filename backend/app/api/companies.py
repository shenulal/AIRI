"""Companies API endpoints."""
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query

from app.database import get_db
from app.models import Company, Document
from app.schemas import (
    CompanyResponse, CompanyCreate, CompanyProfileResponse, DocumentResponse
)
from app.services.company_service import CompanyService

router = APIRouter()
company_service = CompanyService()


@router.get("/", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all companies with pagination."""
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies


@router.post("/", response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
):
    """Create a new company."""
    db_company = company_service.create_company(db, company)
    return db_company


@router.get("/{company_id}", response_model=CompanyProfileResponse)
async def get_company_profile(
    company_id: str,
    db: Session = Depends(get_db),
):
    """Get detailed company profile with summary, risk score, and recent documents."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get recent documents
    recent_docs = (
        db.query(Document)
        .filter(Document.company_id == company_id)
        .order_by(Document.published_at.desc())
        .limit(10)
        .all()
    )
    
    # Build response
    profile = CompanyProfileResponse(
        **{
            "id": company.id,
            "name": company.name,
            "ticker": company.ticker,
            "industry": company.industry,
            "country": company.country,
            "website": company.website,
            "description": company.description,
            "risk_score": company.risk_score,
            "executive_summary": company.executive_summary,
            "created_at": company.created_at,
            "updated_at": company.updated_at,
            "recent_documents": recent_docs,
        }
    )
    
    return profile


@router.get("/{company_id}/documents", response_model=List[DocumentResponse])
async def get_company_documents(
    company_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get documents for a company."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    documents = (
        db.query(Document)
        .filter(Document.company_id == company_id)
        .order_by(Document.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return documents


@router.get("/{company_id}/risk-score")
async def get_company_risk_score(
    company_id: str,
    db: Session = Depends(get_db),
):
    """Get current risk score for a company."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {
        "company_id": company_id,
        "risk_score": company.risk_score,
        "updated_at": company.risk_score_updated_at,
    }


@router.get("/{company_id}/summary")
async def get_company_summary(
    company_id: str,
    db: Session = Depends(get_db),
):
    """Get executive summary for a company."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {
        "company_id": company_id,
        "summary": company.executive_summary,
        "updated_at": company.summary_updated_at,
    }

