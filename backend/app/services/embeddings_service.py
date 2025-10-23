"""Embeddings and RAG service."""
from typing import List, Dict, Any
import numpy as np
from sqlalchemy.orm import Session
import openai

from app.config import get_settings
from app.models import Document, Company

settings = get_settings()
openai.api_key = settings.openai_api_key


class EmbeddingsService:
    """Service for generating and managing embeddings."""
    
    def __init__(self):
        self.model = settings.openai_embedding_model
        self.cache = {}  # Simple in-memory cache
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI."""
        if not settings.openai_api_key:
            print("OpenAI API key not configured")
            return []
        
        try:
            # Check cache
            if text in self.cache:
                return self.cache[text]
            
            # Truncate text
            text = text[:8000]
            
            response = openai.Embedding.create(
                input=text,
                model=self.model,
            )
            
            embedding = response["data"][0]["embedding"]
            self.cache[text] = embedding
            return embedding
        
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    def generate_document_embedding(self, db: Session, document: Document) -> Document:
        """Generate and store embedding for a document."""
        if document.embedding_id:
            return document  # Already has embedding
        
        # Generate embedding
        text = f"{document.title} {document.content}"
        embedding = self.generate_embedding(text)
        
        if embedding:
            # Store embedding ID (in production, store in vector DB)
            document.embedding_id = f"doc_{document.id}"
            db.commit()
        
        return document
    
    def retrieve_similar_documents(
        self, db: Session, company_id: str, query: str, limit: int = 10
    ) -> List[Document]:
        """Retrieve documents similar to query using embeddings."""
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        if not query_embedding:
            # Fallback to keyword search
            return db.query(Document).filter(
                Document.company_id == company_id
            ).order_by(Document.published_at.desc()).limit(limit).all()
        
        # Get all documents for company
        documents = db.query(Document).filter(
            Document.company_id == company_id
        ).all()
        
        # Compute similarity scores (simple cosine similarity)
        scored_docs = []
        for doc in documents:
            if not doc.embedding_id:
                continue
            
            # In production, retrieve embedding from vector DB
            doc_embedding = self.generate_embedding(f"{doc.title} {doc.content}")
            
            if doc_embedding:
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                scored_docs.append((doc, similarity))
        
        # Sort by similarity and return top results
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in scored_docs[:limit]]
    
    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class RAGService:
    """Service for Retrieval-Augmented Generation."""
    
    def __init__(self):
        self.embeddings_service = EmbeddingsService()
    
    def generate_company_summary(
        self, db: Session, company_id: str
    ) -> str:
        """Generate executive summary for a company using RAG."""
        if not settings.openai_api_key:
            return "OpenAI API key not configured"
        
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return "Company not found"
        
        # Retrieve relevant documents
        query = f"Latest news and information about {company.name}"
        documents = self.embeddings_service.retrieve_similar_documents(
            db, company_id, query, limit=10
        )
        
        if not documents:
            return f"No documents found for {company.name}"
        
        # Build context from documents
        context = "\n\n".join([
            f"Title: {doc.title}\nContent: {doc.content[:500]}"
            for doc in documents
        ])
        
        # Generate summary using GPT
        try:
            prompt = f"""Based on the following recent news and information about {company.name}, 
provide a concise 3-4 sentence executive summary:

{context}

Summary:"""
            
            response = openai.ChatCompletion.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst. Provide concise, factual summaries."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.7,
            )
            
            summary = response["choices"][0]["message"]["content"].strip()
            return summary
        
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Unable to generate summary for {company.name}"

