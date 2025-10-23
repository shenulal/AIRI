"""Data ingestion service for external sources."""
import uuid
from datetime import datetime
from typing import List, Dict, Any
import requests
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Company, Document
from app.services.company_service import CompanyService

settings = get_settings()
company_service = CompanyService()


class NewsAPIIngester:
    """Ingest news articles from NewsAPI."""
    
    def __init__(self):
        self.api_key = settings.newsapi_key
        self.base_url = "https://newsapi.org/v2"
    
    def ingest_company_news(
        self, db: Session, company_name: str, limit: int = 10
    ) -> List[Document]:
        """Ingest news articles for a company."""
        if not self.api_key:
            print("NewsAPI key not configured")
            return []
        
        try:
            # Get or create company
            company = company_service.get_or_create_company(db, company_name)
            
            # Fetch articles
            url = f"{self.base_url}/everything"
            params = {
                "q": company_name,
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.api_key,
                "pageSize": limit,
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            documents = []
            for article in data.get("articles", []):
                # Check if document already exists
                existing = db.query(Document).filter(
                    Document.source_url == article.get("url")
                ).first()
                if existing:
                    continue
                
                doc = Document(
                    id=str(uuid.uuid4()),
                    company_id=company.id,
                    title=article.get("title", ""),
                    content=article.get("content", "") or article.get("description", ""),
                    source="newsapi",
                    source_url=article.get("url"),
                    published_at=datetime.fromisoformat(
                        article.get("publishedAt", "").replace("Z", "+00:00")
                    ) if article.get("publishedAt") else None,
                )
                db.add(doc)
                documents.append(doc)
            
            db.commit()
            print(f"Ingested {len(documents)} articles for {company_name}")
            return documents
        
        except Exception as e:
            print(f"Error ingesting news for {company_name}: {e}")
            return []


class OpenCorporatesIngester:
    """Ingest company data from OpenCorporates."""
    
    def __init__(self):
        self.base_url = "https://api.opencorporates.com/v0.4"
    
    def search_company(self, db: Session, company_name: str) -> Company:
        """Search and ingest company from OpenCorporates."""
        try:
            url = f"{self.base_url}/companies/search"
            params = {
                "q": company_name,
                "per_page": 1,
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            companies = data.get("companies", [])
            if not companies:
                # Create company with just the name
                return company_service.get_or_create_company(db, company_name)
            
            company_data = companies[0].get("company", {})
            
            # Get or create company
            company = company_service.get_or_create_company(
                db,
                company_name=company_data.get("name", company_name),
                country=company_data.get("jurisdiction_code"),
            )
            
            print(f"Ingested company data for {company_name}")
            return company
        
        except Exception as e:
            print(f"Error ingesting company from OpenCorporates: {e}")
            return company_service.get_or_create_company(db, company_name)


class IngestionService:
    """Main ingestion service."""
    
    def __init__(self):
        self.newsapi = NewsAPIIngester()
        self.opencorporates = OpenCorporatesIngester()
    
    def ingest_company(self, db: Session, company_name: str) -> Dict[str, Any]:
        """Ingest company data from all sources."""
        # Get company from OpenCorporates
        company = self.opencorporates.search_company(db, company_name)
        
        # Ingest news articles
        documents = self.newsapi.ingest_company_news(db, company_name)
        
        return {
            "company": company,
            "documents": documents,
            "document_count": len(documents),
        }

