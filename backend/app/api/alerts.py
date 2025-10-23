"""Alerts API endpoints."""
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Header
import uuid

from app.database import get_db
from app.models import Alert, Watchlist
from app.schemas import AlertResponse, AlertCreate

router = APIRouter()


def get_user_id(authorization: str = Header(None)) -> str:
    """Extract user ID from authorization header (simplified for MVP)."""
    if not authorization:
        return "default-user"
    return authorization.replace("Bearer ", "")


@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """List all alerts for the user."""
    alerts = db.query(Alert).filter(Alert.user_id == user_id).all()
    return alerts


@router.post("/subscribe", response_model=AlertResponse)
async def subscribe_to_alerts(
    alert: AlertCreate,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """Subscribe to alerts for a watchlist or company."""
    # Validate watchlist if provided
    if alert.watchlist_id:
        watchlist = db.query(Watchlist).filter(
            Watchlist.id == alert.watchlist_id,
            Watchlist.user_id == user_id,
        ).first()
        if not watchlist:
            raise HTTPException(status_code=404, detail="Watchlist not found")
    
    db_alert = Alert(
        id=str(uuid.uuid4()),
        user_id=user_id,
        watchlist_id=alert.watchlist_id,
        email=alert.email,
        alert_type=alert.alert_type,
        threshold=alert.threshold,
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.patch("/{alert_id}")
async def update_alert(
    alert_id: str,
    is_active: bool,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """Update alert status."""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == user_id,
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_active = is_active
    db.commit()
    
    return {"message": "Alert updated"}


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    user_id: str = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    """Delete an alert."""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == user_id,
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    
    return {"message": "Alert deleted"}

