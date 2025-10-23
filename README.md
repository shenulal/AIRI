# AIRI: AI Insights & Risk Intelligence Platform

A minimum-viable AI-powered platform for ingesting public company data, analyzing sentiment, computing risk scores, and providing actionable intelligence via REST API and React dashboard.

## Features

- **Multi-source Data Ingestion**: NewsAPI (news articles) + OpenCorporates (company registry)
- **NLP Pipeline**: Named Entity Recognition (NER), sentiment analysis, embeddings
- **Risk Scoring**: Hybrid rule-based + ML (logistic regression) scoring
- **RAG Summarization**: LLM-based executive summaries using semantic retrieval
- **REST API**: Search, company profiles, watchlists, alerts
- **React Dashboard**: Search, profiles, sentiment timelines, watchlists
- **Email Alerts**: SendGrid integration for watchlist notifications

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AIRI Platform                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  NewsAPI     │  │OpenCorporates│  │  Custom      │       │
│  │  Ingestion   │  │  Ingestion   │  │  Sources     │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                  │               │
│         └─────────────────┼──────────────────┘               │
│                           │                                  │
│                    ┌──────▼──────┐                           │
│                    │ Normalization│                          │
│                    │  Pipeline    │                          │
│                    └──────┬───────┘                          │
│                           │                                  │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│    ┌────▼────┐    ┌──────▼──────┐   ┌─────▼────┐           │
│    │PostgreSQL│    │ Elasticsearch│   │ Pinecone │           │
│    │(Canonical)    │ (Full-text)  │   │(Embeddings)         │
│    └────┬────┘    └──────┬──────┘   └─────┬────┘           │
│         │                 │               │                 │
│         └─────────────────┼───────────────┘                 │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│    ┌────▼────┐    ┌──────▼──────┐   ┌─────▼────┐           │
│    │NLP Pipe │    │Risk Scoring  │   │RAG Engine│           │
│    │(NER,    │    │(Rules + ML)  │   │(LLM)     │           │
│    │Sentiment)    └──────┬──────┘   └─────┬────┘           │
│    └────┬────┘           │               │                 │
│         └─────────────────┼───────────────┘                 │
│                           │                                 │
│                    ┌──────▼──────┐                          │
│                    │  FastAPI    │                          │
│                    │  REST API   │                          │
│                    └──────┬───────┘                         │
│                           │                                 │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│    ┌────▼────┐    ┌──────▼──────┐   ┌─────▼────┐           │
│    │React    │    │SendGrid      │   │Monitoring│           │
│    │Dashboard│    │Alerts        │   │& Logging │           │
│    └─────────┘    └──────────────┘   └──────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- API Keys: OpenAI, NewsAPI, SendGrid (optional)

### Setup

```bash
# Clone and navigate
cd AIRI

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend python -m alembic upgrade head

# Load sample data
docker-compose exec backend python scripts/load_sample_data.py

# Start frontend dev server
cd frontend && npm install && npm run dev
```

### API Endpoints

- `GET /api/companies/search?q=...` - Search companies
- `GET /api/companies/{id}` - Get company profile with summary & risk score
- `POST /api/watchlists` - Create watchlist
- `POST /api/alerts/subscribe` - Subscribe to alerts
- `GET /api/health` - Health check

### Dashboard

Open `http://localhost:3000` to access the React dashboard.

## Project Structure

```
AIRI/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # REST endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── pipelines/      # NLP, ingestion, risk scoring
│   │   └── config.py       # Configuration
│   ├── tests/              # Unit & integration tests
│   ├── scripts/            # Data loading, migrations
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Local dev environment
├── .env.example            # Environment template
└── README.md               # This file
```

## Development

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

See `DEPLOYMENT.md` for production deployment guides (Docker, Kubernetes).

## Contributing

1. Create a feature branch
2. Write tests
3. Submit PR with description

## License

MIT

