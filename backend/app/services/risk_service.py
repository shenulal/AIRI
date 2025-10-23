"""Risk scoring service."""
from typing import Dict, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import re

from app.models import Company, Document, RiskScore
from app.services.nlp_service import NLPService

nlp_service = NLPService()

# Risk keywords
BANKRUPTCY_KEYWORDS = [
    "bankruptcy", "insolvency", "liquidation", "restructuring",
    "debt default", "credit downgrade", "financial distress"
]

LEGAL_KEYWORDS = [
    "lawsuit", "litigation", "settlement", "fine", "penalty",
    "investigation", "regulatory action", "compliance violation"
]

NEGATIVE_KEYWORDS = [
    "loss", "decline", "layoff", "closure", "shutdown",
    "recall", "scandal", "fraud", "corruption"
]


class RiskScoringService:
    """Service for computing risk scores."""
    
    def compute_rule_based_score(self, db: Session, company_id: str) -> float:
        """Compute rule-based risk score."""
        score = 0.0
        
        # Get recent documents (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        documents = db.query(Document).filter(
            Document.company_id == company_id,
            Document.published_at >= thirty_days_ago,
        ).all()
        
        if not documents:
            return score
        
        # Check for bankruptcy/legal keywords
        for doc in documents:
            content = (doc.title + " " + doc.content).lower()
            
            if any(kw in content for kw in BANKRUPTCY_KEYWORDS):
                score += 30
            
            if any(kw in content for kw in LEGAL_KEYWORDS):
                score += 20
            
            if any(kw in content for kw in NEGATIVE_KEYWORDS):
                score += 10
        
        # Normalize by document count
        if documents:
            score = score / len(documents)
        
        # Cap at 100
        return min(score, 100.0)
    
    def compute_ml_score(self, db: Session, company_id: str) -> float:
        """Compute ML-based risk score using simple logistic regression."""
        # Get features
        features = self._extract_features(db, company_id)
        
        # Simple logistic regression weights (trained on simulated data)
        weights = {
            "negative_sentiment_fraction": 40.0,
            "mention_count": 5.0,
            "negative_document_count": 15.0,
        }
        
        # Compute score
        score = 0.0
        for feature, weight in weights.items():
            score += features.get(feature, 0.0) * weight
        
        # Sigmoid to normalize to 0-100
        import math
        sigmoid_score = 100.0 / (1.0 + math.exp(-score / 50.0))
        
        return sigmoid_score
    
    def _extract_features(self, db: Session, company_id: str) -> Dict[str, float]:
        """Extract features for ML scoring."""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        documents = db.query(Document).filter(
            Document.company_id == company_id,
            Document.published_at >= thirty_days_ago,
        ).all()
        
        if not documents:
            return {
                "negative_sentiment_fraction": 0.0,
                "mention_count": 0.0,
                "negative_document_count": 0.0,
            }
        
        # Compute features
        negative_count = sum(1 for d in documents if d.sentiment_label == "negative")
        negative_fraction = negative_count / len(documents) if documents else 0.0
        
        return {
            "negative_sentiment_fraction": negative_fraction,
            "mention_count": len(documents),
            "negative_document_count": negative_count,
        }
    
    def compute_risk_score(self, db: Session, company_id: str) -> Tuple[float, Dict[str, Any]]:
        """Compute composite risk score."""
        rule_score = self.compute_rule_based_score(db, company_id)
        ml_score = self.compute_ml_score(db, company_id)
        
        # Weighted average (60% rule, 40% ML)
        composite_score = (rule_score * 0.6) + (ml_score * 0.4)
        
        features = self._extract_features(db, company_id)
        
        return composite_score, {
            "rule_score": rule_score,
            "ml_score": ml_score,
            "features": features,
        }
    
    def update_company_risk_score(self, db: Session, company_id: str) -> Company:
        """Update company risk score and store history."""
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return None
        
        # Compute new score
        score, details = self.compute_risk_score(db, company_id)
        
        # Update company
        company.risk_score = score
        company.risk_score_updated_at = datetime.utcnow()
        
        # Store in history
        risk_record = RiskScore(
            id=f"risk_{company_id}_{datetime.utcnow().timestamp()}",
            company_id=company_id,
            score=score,
            rule_score=details["rule_score"],
            ml_score=details["ml_score"],
            features=details["features"],
        )
        
        db.add(risk_record)
        db.commit()
        db.refresh(company)
        
        return company

