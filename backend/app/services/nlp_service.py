"""NLP pipeline service for sentiment analysis and NER."""
from typing import Dict, List, Any, Tuple
import spacy
from transformers import pipeline
from sqlalchemy.orm import Session

from app.models import Document

# Load models
nlp = None
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model 'en_core_web_sm' not found. NER will be disabled.")
    print("To enable NER, run: python -m spacy download en_core_web_sm")
    nlp = None

# Sentiment analysis pipeline
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


class NLPService:
    """Service for NLP operations."""
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text using spaCy."""
        if nlp is None:
            return {}

        try:
            doc = nlp(text)
            entities = {}

            for ent in doc.ents:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)

            return entities
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return {}
    
    def compute_sentiment(self, text: str) -> Tuple[float, str]:
        """Compute sentiment score and label for text."""
        try:
            # Truncate text to avoid token limit
            text = text[:512]
            
            result = sentiment_pipeline(text)[0]
            label = result["label"].lower()
            score = result["score"]
            
            # Convert to -1 to 1 scale
            if label == "negative":
                sentiment_score = -score
            else:
                sentiment_score = score
            
            # Map to label
            if sentiment_score > 0.5:
                sentiment_label = "positive"
            elif sentiment_score < -0.5:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            return sentiment_score, sentiment_label
        
        except Exception as e:
            print(f"Error computing sentiment: {e}")
            return 0.0, "neutral"
    
    def process_document(self, db: Session, document: Document) -> Document:
        """Process a document with NLP pipeline."""
        # Extract entities
        entities = self.extract_entities(document.content)
        document.entities = entities
        
        # Compute sentiment
        sentiment_score, sentiment_label = self.compute_sentiment(document.content)
        document.sentiment_score = sentiment_score
        document.sentiment_label = sentiment_label
        
        db.commit()
        return document
    
    def process_company_documents(self, db: Session, company_id: str) -> int:
        """Process all documents for a company."""
        documents = db.query(Document).filter(
            Document.company_id == company_id,
            Document.sentiment_score.is_(None),
        ).all()
        
        for doc in documents:
            self.process_document(db, doc)
        
        return len(documents)
    
    def get_company_sentiment_stats(self, db: Session, company_id: str) -> Dict[str, Any]:
        """Get sentiment statistics for a company."""
        documents = db.query(Document).filter(
            Document.company_id == company_id,
            Document.sentiment_score.isnot(None),
        ).all()
        
        if not documents:
            return {
                "avg_sentiment": 0.0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
                "total_count": 0,
            }
        
        sentiments = [d.sentiment_score for d in documents]
        labels = [d.sentiment_label for d in documents]
        
        return {
            "avg_sentiment": sum(sentiments) / len(sentiments),
            "positive_count": labels.count("positive"),
            "negative_count": labels.count("negative"),
            "neutral_count": labels.count("neutral"),
            "total_count": len(documents),
        }

