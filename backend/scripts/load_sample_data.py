"""Script to load sample data into the database."""
import sys
import os
from datetime import datetime, timedelta
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Company, Document
from app.services.ingestion_service import IngestionService
from app.services.nlp_service import NLPService
from app.services.risk_service import RiskScoringService

# Initialize services
ingestion_service = IngestionService()
nlp_service = NLPService()
risk_service = RiskScoringService()


def create_sample_companies(db: Session):
    """Create sample companies."""
    companies = [
        {
            "name": "Apple Inc.",
            "ticker": "AAPL",
            "industry": "Technology",
            "country": "US",
            "website": "https://www.apple.com",
            "description": "Apple Inc. is an American technology company that designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and software services.",
        },
        {
            "name": "Tesla Inc.",
            "ticker": "TSLA",
            "industry": "Automotive",
            "country": "US",
            "website": "https://www.tesla.com",
            "description": "Tesla, Inc. is an American electric vehicle and clean energy company.",
        },
        {
            "name": "Microsoft Corporation",
            "ticker": "MSFT",
            "industry": "Technology",
            "country": "US",
            "website": "https://www.microsoft.com",
            "description": "Microsoft Corporation is an American technology corporation that develops, manufactures, licenses, supports, and sells computer software, consumer electronics, personal computers, and related services.",
        },
    ]
    
    created = []
    for company_data in companies:
        existing = db.query(Company).filter(Company.name == company_data["name"]).first()
        if existing:
            print(f"Company {company_data['name']} already exists")
            created.append(existing)
            continue
        
        company = Company(
            id=str(uuid.uuid4()),
            **company_data,
        )
        db.add(company)
        created.append(company)
    
    db.commit()
    print(f"Created {len(created)} companies")
    return created


def create_sample_documents(db: Session, companies: list):
    """Create sample documents for companies."""
    sample_docs = [
        {
            "title": "Apple Reports Record Q4 Revenue",
            "content": "Apple Inc. announced record revenue for Q4 2024, driven by strong iPhone sales and services growth. The company's financial performance exceeded analyst expectations.",
            "source": "newsapi",
            "sentiment": "positive",
        },
        {
            "title": "Tesla Faces Production Challenges",
            "content": "Tesla reported production delays at its Berlin and Austin factories due to supply chain disruptions. The company is working to resolve the issues.",
            "source": "newsapi",
            "sentiment": "negative",
        },
        {
            "title": "Microsoft Expands AI Capabilities",
            "content": "Microsoft announced new AI features in Office 365 and Azure, positioning itself as a leader in enterprise AI solutions.",
            "source": "newsapi",
            "sentiment": "positive",
        },
    ]
    
    created = []
    for i, company in enumerate(companies):
        doc_data = sample_docs[i % len(sample_docs)]
        
        document = Document(
            id=str(uuid.uuid4()),
            company_id=company.id,
            title=doc_data["title"],
            content=doc_data["content"],
            source=doc_data["source"],
            source_url=f"https://example.com/article-{i}",
            published_at=datetime.utcnow() - timedelta(days=i),
        )
        db.add(document)
        created.append(document)
    
    db.commit()
    print(f"Created {len(created)} documents")
    return created


def process_documents_nlp(db: Session, documents: list):
    """Process documents with NLP pipeline."""
    for doc in documents:
        nlp_service.process_document(db, doc)
    print(f"Processed {len(documents)} documents with NLP")


def compute_risk_scores(db: Session, companies: list):
    """Compute risk scores for companies."""
    for company in companies:
        risk_service.update_company_risk_score(db, company.id)
    print(f"Computed risk scores for {len(companies)} companies")


def main():
    """Main function."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("\nLoading sample data...")
        
        # Create companies
        companies = create_sample_companies(db)
        
        # Create documents
        documents = create_sample_documents(db, companies)
        
        # Process with NLP
        process_documents_nlp(db, documents)
        
        # Compute risk scores
        compute_risk_scores(db, companies)
        
        print("\n✓ Sample data loaded successfully!")
        
        # Print summary
        print("\nSummary:")
        for company in companies:
            db.refresh(company)
            print(f"  - {company.name} ({company.ticker}): Risk Score = {company.risk_score:.2f}")
    
    except Exception as e:
        print(f"Error loading sample data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()

