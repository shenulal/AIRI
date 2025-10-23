"""Tests for API endpoints."""
import uuid
from app.models import Company, Document


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "unhealthy"]
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_create_company(client, db):
    """Test creating a company."""
    response = client.post(
        "/api/companies/",
        json={
            "name": "Test Company",
            "ticker": "TEST",
            "industry": "Technology",
            "country": "US",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Company"
    assert data["ticker"] == "TEST"
    assert "id" in data


def test_list_companies(client, db):
    """Test listing companies."""
    # Create a company
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
        ticker="TEST",
    )
    db.add(company)
    db.commit()
    
    response = client.get("/api/companies/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(c["name"] == "Test Company" for c in data)


def test_get_company(client, db):
    """Test getting a company."""
    company = Company(
        id=str(uuid.uuid4()),
        name="Test Company",
        ticker="TEST",
        risk_score=50.0,
    )
    db.add(company)
    db.commit()
    
    response = client.get(f"/api/companies/{company.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Company"
    assert data["risk_score"] == 50.0


def test_search_companies(client, db):
    """Test searching companies."""
    company = Company(
        id=str(uuid.uuid4()),
        name="Apple Inc.",
        ticker="AAPL",
    )
    db.add(company)
    db.commit()
    
    response = client.get("/api/search/companies?q=Apple")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any(c["name"] == "Apple Inc." for c in data["results"])


def test_get_company_documents(client, db):
    """Test getting company documents."""
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
        content="Test content",
        source="newsapi",
    )
    db.add(doc)
    db.commit()
    
    response = client.get(f"/api/companies/{company.id}/documents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Article"


def test_create_watchlist(client):
    """Test creating a watchlist."""
    response = client.post(
        "/api/watchlists/",
        json={
            "name": "My Watchlist",
            "description": "Test watchlist",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "My Watchlist"
    assert "id" in data


def test_list_watchlists(client, db):
    """Test listing watchlists."""
    response = client.get("/api/watchlists/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_subscribe_to_alerts(client):
    """Test subscribing to alerts."""
    response = client.post(
        "/api/alerts/subscribe",
        json={
            "email": "test@example.com",
            "alert_type": "risk_increase",
            "threshold": 70,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["alert_type"] == "risk_increase"


def test_list_alerts(client):
    """Test listing alerts."""
    response = client.get("/api/alerts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

