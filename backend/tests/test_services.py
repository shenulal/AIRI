"""Tests for services."""
import uuid
from app.models import Company, Document
from app.services.company_service import CompanyService
from app.services.nlp_service import NLPService
from app.services.risk_service import RiskScoringService
from app.schemas import CompanyCreate


def test_create_company_service(db):
    """Test company service create."""
    service = CompanyService()
    company_data = CompanyCreate(
        name="Test Company",
        ticker="TEST",
        industry="Tech",
    )
    
    company = service.create_company(db, company_data)
    assert company.name == "Test Company"
    assert company.ticker == "TEST"
    assert company.id is not None


def test_get_or_create_company(db):
    """Test get or create company."""
    service = CompanyService()
    
    # Create first time
    company1 = service.get_or_create_company(db, "Test Company")
    assert company1.name == "Test Company"
    
    # Get existing
    company2 = service.get_or_create_company(db, "Test Company")
    assert company1.id == company2.id


def test_update_company_risk_score(db):
    """Test updating company risk score."""
    service = CompanyService()
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
        risk_score=0.0,
    )
    db.add(company)
    db.commit()
    
    updated = service.update_company_risk_score(db, company.id, 75.5)
    assert updated.risk_score == 75.5


def test_nlp_extract_entities(db):
    """Test NLP entity extraction."""
    service = NLPService()
    text = "Apple Inc. is a technology company founded by Steve Jobs."
    
    entities = service.extract_entities(text)
    assert "ORG" in entities or "PERSON" in entities


def test_nlp_compute_sentiment(db):
    """Test sentiment analysis."""
    service = NLPService()
    
    positive_text = "This is great news! The company is doing very well."
    score, label = service.compute_sentiment(positive_text)
    assert label in ["positive", "negative", "neutral"]
    assert -1 <= score <= 1


def test_nlp_process_document(db):
    """Test document processing."""
    service = NLPService()
    
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
    )
    db.add(company)
    db.commit()
    
    doc = Document(
        id=str(uuid.uuid4()),
        company_id=company.id,
        title="Test Article",
        content="This is a positive article about the company.",
        source="newsapi",
    )
    db.add(doc)
    db.commit()
    
    processed = service.process_document(db, doc)
    assert processed.sentiment_score is not None
    assert processed.sentiment_label is not None


def test_risk_scoring_rule_based(db):
    """Test rule-based risk scoring."""
    service = RiskScoringService()
    
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
    )
    db.add(company)
    db.commit()
    
    # Create a document with negative keywords
    doc = Document(
        id=str(uuid.uuid4()),
        company_id=company.id,
        title="Company Bankruptcy Filing",
        content="The company filed for bankruptcy due to financial distress.",
        source="newsapi",
    )
    db.add(doc)
    db.commit()
    
    score = service.compute_rule_based_score(db, company.id)
    assert 0 <= score <= 100


def test_risk_scoring_ml_based(db):
    """Test ML-based risk scoring."""
    service = RiskScoringService()
    
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
    )
    db.add(company)
    db.commit()
    
    score = service.compute_ml_score(db, company.id)
    assert 0 <= score <= 100


def test_compute_composite_risk_score(db):
    """Test composite risk score."""
    service = RiskScoringService()
    
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
    )
    db.add(company)
    db.commit()
    
    score, details = service.compute_risk_score(db, company.id)
    assert 0 <= score <= 100
    assert "rule_score" in details
    assert "ml_score" in details
    assert "features" in details


def test_update_company_risk_score_service(db):
    """Test updating company risk score via service."""
    service = RiskScoringService()
    
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
    )
    db.add(company)
    db.commit()
    
    updated = service.update_company_risk_score(db, company.id)
    assert updated is not None
    assert updated.risk_score >= 0

