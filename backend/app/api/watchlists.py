"""Watchlists API endpoints."""
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Header
import uuid

from app.database import get_db
from app.models import Watchlist, WatchlistItem, Company
from app.schemas import (
    WatchlistResponse, WatchlistCreate, WatchlistAddCompanyRequest
)

router = APIRouter()


def get_user_id(authorization: str = Header(None)) -> str:
    """Extract user ID from authorization header (simplified for MVP)."""
    # In production, validate JWT token
    if not authorization:
        return "default-user"
    return authorization.replace("Bearer ", "")


@router.get("/", response_model=List[WatchlistResponse])
async def list_watchlists(
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """List all watchlists for the user."""
    watchlists = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()
    return watchlists


@router.post("/", response_model=WatchlistResponse)
async def create_watchlist(
    watchlist: WatchlistCreate,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """Create a new watchlist."""
    db_watchlist = Watchlist(
        id=str(uuid.uuid4()),
        user_id=user_id,
        name=watchlist.name,
        description=watchlist.description,
    )
    db.add(db_watchlist)
    db.commit()
    db.refresh(db_watchlist)
    return db_watchlist


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
async def get_watchlist(
    watchlist_id: str,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """Get a specific watchlist."""
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user_id,
    ).first()
    
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    return watchlist


@router.post("/{watchlist_id}/companies")
async def add_company_to_watchlist(
    watchlist_id: str,
    request: WatchlistAddCompanyRequest,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """Add a company to a watchlist."""
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user_id,
    ).first()
    
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    company = db.query(Company).filter(Company.id == request.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Check if already in watchlist
    existing = db.query(WatchlistItem).filter(
        WatchlistItem.watchlist_id == watchlist_id,
        WatchlistItem.company_id == request.company_id,
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Company already in watchlist")
    
    item = WatchlistItem(
        id=str(uuid.uuid4()),
        watchlist_id=watchlist_id,
        company_id=request.company_id,
    )
    db.add(item)
    db.commit()
    
    return {"message": "Company added to watchlist"}


@router.delete("/{watchlist_id}/companies/{company_id}")
async def remove_company_from_watchlist(
    watchlist_id: str,
    company_id: str,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """Remove a company from a watchlist."""
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user_id,
    ).first()
    
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    item = db.query(WatchlistItem).filter(
        WatchlistItem.watchlist_id == watchlist_id,
        WatchlistItem.company_id == company_id,
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Company not in watchlist")
    
    db.delete(item)
    db.commit()
    
    return {"message": "Company removed from watchlist"}

