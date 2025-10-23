"""Company service for business logic."""
import uuid
from sqlalchemy.orm import Session

from app.models import Company
from app.schemas import CompanyCreate


class CompanyService:
    """Service for company operations."""
    
    def create_company(self, db: Session, company: CompanyCreate) -> Company:
        """Create a new company."""
        db_company = Company(
            id=str(uuid.uuid4()),
            name=company.name,
            ticker=company.ticker,
            industry=company.industry,
            country=company.country,
            website=company.website,
            description=company.description,
        )
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company
    
    def get_or_create_company(self, db: Session, name: str, **kwargs) -> Company:
        """Get existing company or create new one."""
        company = db.query(Company).filter(Company.name == name).first()
        if company:
            return company
        
        company_data = CompanyCreate(name=name, **kwargs)
        return self.create_company(db, company_data)
    
    def update_company_risk_score(
        self, db: Session, company_id: str, risk_score: float
    ) -> Company:
        """Update company risk score."""
        company = db.query(Company).filter(Company.id == company_id).first()
        if company:
            company.risk_score = risk_score
            db.commit()
            db.refresh(company)
        return company
    
    def update_company_summary(
        self, db: Session, company_id: str, summary: str
    ) -> Company:
        """Update company executive summary."""
        from datetime import datetime
        company = db.query(Company).filter(Company.id == company_id).first()
        if company:
            company.executive_summary = summary
            company.summary_updated_at = datetime.utcnow()
            db.commit()
            db.refresh(company)
        return company

