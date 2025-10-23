"""Elasticsearch service for full-text search."""
from typing import List, Dict, Any
from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Document

settings = get_settings()


class ElasticsearchService:
    """Service for Elasticsearch operations."""
    
    def __init__(self):
        try:
            self.es = Elasticsearch([settings.elasticsearch_url])
            self.index_name = "airi-documents"
            self._create_index()
        except Exception as e:
            print(f"Warning: Elasticsearch not available: {e}")
            self.es = None
    
    def _create_index(self):
        """Create index if it doesn't exist."""
        if not self.es:
            return
        
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(
                    index=self.index_name,
                    body={
                        "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 0,
                        },
                        "mappings": {
                            "properties": {
                                "document_id": {"type": "keyword"},
                                "company_id": {"type": "keyword"},
                                "title": {"type": "text"},
                                "content": {"type": "text"},
                                "source": {"type": "keyword"},
                                "published_at": {"type": "date"},
                                "ingested_at": {"type": "date"},
                            }
                        },
                    },
                )
        except Exception as e:
            print(f"Error creating Elasticsearch index: {e}")
    
    def index_document(self, document: Document) -> bool:
        """Index a document in Elasticsearch."""
        if not self.es:
            return False
        
        try:
            self.es.index(
                index=self.index_name,
                id=document.id,
                body={
                    "document_id": document.id,
                    "company_id": document.company_id,
                    "title": document.title,
                    "content": document.content,
                    "source": document.source,
                    "published_at": document.published_at,
                    "ingested_at": document.ingested_at,
                },
            )
            return True
        except Exception as e:
            print(f"Error indexing document: {e}")
            return False
    
    def search_documents(
        self, query: str, company_id: str = None, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search documents in Elasticsearch."""
        if not self.es:
            return []
        
        try:
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["title^2", "content"],
                                }
                            }
                        ],
                    }
                },
                "size": limit,
            }
            
            if company_id:
                search_body["query"]["bool"]["filter"] = [
                    {"term": {"company_id": company_id}}
                ]
            
            results = self.es.search(index=self.index_name, body=search_body)
            
            return [hit["_source"] for hit in results["hits"]["hits"]]
        
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from Elasticsearch."""
        if not self.es:
            return False
        
        try:
            self.es.delete(index=self.index_name, id=document_id)
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False

