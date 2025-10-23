"""Search API endpoints."""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.models import Company
from app.schemas import SearchResponse, CompanyResponse

router = APIRouter()


@router.get("/companies", response_model=SearchResponse)
async def search_companies(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search companies by name, ticker, or description."""
    # Build search query
    search_term = f"%{q}%"
    query = db.query(Company).filter(
        or_(
            Company.name.ilike(search_term),
            Company.ticker.ilike(search_term),
            Company.description.ilike(search_term),
        )
    )
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    results = query.offset(skip).limit(limit).all()
    
    return SearchResponse(
        total=total,
        results=results,
        query=q,
    )


@router.get("/documents")
async def search_documents(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search documents by title or content."""
    from app.models import Document
    
    search_term = f"%{q}%"
    query = db.query(Document).filter(
        or_(
            Document.title.ilike(search_term),
            Document.content.ilike(search_term),
        )
    )
    
    total = query.count()
    results = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "results": results,
        "query": q,
    }

