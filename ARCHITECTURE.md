# AIRI Architecture

## System Overview

AIRI is a distributed system for ingesting, analyzing, and providing intelligence on public companies. The architecture follows a microservices-inspired design with clear separation of concerns.

## Components

### 1. Data Ingestion Layer
- **NewsAPI Ingester**: Fetches news articles about companies
- **OpenCorporates Ingester**: Retrieves company registry data
- **Normalization Pipeline**: Standardizes data from multiple sources

### 2. Storage Layer
- **PostgreSQL**: Canonical company records, documents, risk scores, watchlists
- **Elasticsearch**: Full-text search index for documents
- **Pinecone/Milvus**: Vector embeddings for semantic search
- **Redis**: Caching layer for performance

### 3. Processing Layer
- **NLP Pipeline**: 
  - Named Entity Recognition (NER) using spaCy
  - Sentiment analysis using transformers
  - Entity extraction and linking
- **Embeddings Service**: 
  - Text embeddings using OpenAI API
  - Semantic similarity computation
- **Risk Scoring Engine**:
  - Rule-based scoring (keywords, patterns)
  - ML-based scoring (logistic regression)
  - Composite scoring (weighted average)

### 4. RAG & LLM Layer
- **Retrieval-Augmented Generation**:
  - Semantic document retrieval
  - Context building from top-K documents
  - LLM-based summary generation
- **OpenAI Integration**:
  - GPT-3.5-turbo for summaries
  - Text embeddings for semantic search

### 5. API Layer
- **FastAPI Backend**:
  - RESTful endpoints for companies, documents, watchlists, alerts
  - JWT authentication (simplified for MVP)
  - Request validation with Pydantic
  - CORS support

### 6. Frontend Layer
- **React Dashboard**:
  - Company search and profiles
  - Sentiment timeline visualization
  - Watchlist management
  - Alert configuration
  - Responsive design with Tailwind CSS

## Data Flow

```
External Sources (NewsAPI, OpenCorporates)
    ↓
Ingestion Service
    ↓
Normalization & Deduplication
    ↓
PostgreSQL (Canonical Store)
    ↓
    ├→ Elasticsearch (Full-text Index)
    ├→ NLP Pipeline (Sentiment, NER)
    ├→ Embeddings Service (Vector DB)
    └→ Risk Scoring Engine
    ↓
API Layer (FastAPI)
    ↓
Frontend (React)
```

## Database Schema

### Core Tables
- **companies**: Canonical company records
- **documents**: Raw ingested documents
- **risk_scores**: Historical risk scores
- **sentiment_timeseries**: Aggregated sentiment over time

### User Management
- **watchlists**: User watchlists
- **watchlist_items**: Companies in watchlists
- **alerts**: Alert subscriptions

## API Endpoints

### Companies
- `GET /api/companies` - List companies
- `POST /api/companies` - Create company
- `GET /api/companies/{id}` - Get company profile
- `GET /api/companies/{id}/documents` - Get documents
- `GET /api/companies/{id}/risk-score` - Get risk score
- `GET /api/companies/{id}/summary` - Get summary

### Search
- `GET /api/search/companies?q=...` - Search companies
- `GET /api/search/documents?q=...` - Search documents

### Watchlists
- `GET /api/watchlists` - List watchlists
- `POST /api/watchlists` - Create watchlist
- `GET /api/watchlists/{id}` - Get watchlist
- `POST /api/watchlists/{id}/companies` - Add company
- `DELETE /api/watchlists/{id}/companies/{company_id}` - Remove company

### Alerts
- `GET /api/alerts` - List alerts
- `POST /api/alerts/subscribe` - Subscribe to alerts
- `PATCH /api/alerts/{id}` - Update alert
- `DELETE /api/alerts/{id}` - Delete alert

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Search**: Elasticsearch
- **Vector DB**: Pinecone/Milvus
- **Cache**: Redis
- **NLP**: spaCy, transformers
- **LLM**: OpenAI API
- **ORM**: SQLAlchemy
- **Migrations**: Alembic

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Routing**: React Router
- **Charts**: Recharts

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose (dev), Kubernetes (prod)
- **CI/CD**: GitHub Actions
- **Testing**: pytest, Jest

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers behind load balancer
- Managed database services (RDS, Cloud SQL)
- Managed search (Elasticsearch Cloud)
- Managed vector DB (Pinecone)

### Caching Strategy
- Redis for frequently accessed data
- Embedding cache to avoid recomputation
- HTTP caching headers

### Batch Processing
- Async ingestion jobs
- Scheduled risk score updates
- Batch embedding generation

## Security

### Authentication
- JWT tokens for API access
- User context in headers
- Simplified for MVP (no OAuth)

### Data Protection
- Environment variables for secrets
- Database encryption at rest
- HTTPS/TLS in production
- SQL injection prevention (SQLAlchemy ORM)

### Rate Limiting
- API rate limits per user
- NewsAPI rate limit handling
- Elasticsearch query limits

## Monitoring & Observability

### Logging
- Structured logging with JSON
- Log aggregation ready
- Request/response logging

### Metrics
- API response times
- Database query performance
- Cache hit rates
- Error rates

### Health Checks
- `/api/health` endpoint
- Database connectivity check
- Elasticsearch cluster health

## Future Enhancements

1. **Advanced ML**:
   - Time-series forecasting for risk
   - Anomaly detection
   - Clustering for company similarity

2. **Real-time Updates**:
   - WebSocket support for live updates
   - Event streaming (Kafka)
   - Real-time alerts

3. **Advanced Search**:
   - Faceted search
   - Saved searches
   - Search suggestions

4. **Compliance**:
   - Audit logging
   - Data retention policies
   - GDPR compliance

5. **Integration**:
   - Slack notifications
   - Email digests
   - Third-party API integrations

