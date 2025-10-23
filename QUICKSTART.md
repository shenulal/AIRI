# AIRI Quick Start Guide

Get AIRI running locally in 5 minutes!

## Prerequisites

- Docker & Docker Compose
- Git
- API Keys (optional for MVP):
  - OpenAI API key (for summaries)
  - NewsAPI key (for news ingestion)

## Step 1: Clone & Setup

```bash
# Clone the repository
git clone <repo-url>
cd AIRI

# Copy environment file
cp .env.example .env
```

## Step 2: Configure API Keys (Optional)

Edit `.env` and add your API keys:

```bash
# For LLM summaries (optional)
OPENAI_API_KEY=sk-...

# For news ingestion (optional)
NEWSAPI_KEY=...

# For email alerts (optional)
SENDGRID_API_KEY=...
```

**Note**: The MVP works without these keys - you'll just get sample data.

## Step 3: Start Services

```bash
# Start all services (PostgreSQL, Redis, Elasticsearch, Backend, Frontend)
docker-compose up -d

# Wait for services to be healthy (30-60 seconds)
docker-compose ps
```

## Step 4: Initialize Database

```bash
# Run migrations
docker-compose exec backend python -m alembic upgrade head

# Load sample data
docker-compose exec backend python scripts/load_sample_data.py
```

## Step 5: Access the Application

Open your browser:

- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/api/health

## What's Included

### Sample Data
- 3 companies (Apple, Tesla, Microsoft)
- 3 news articles
- Sentiment analysis
- Risk scores

### Features to Try

1. **Search Companies**
   - Go to Search page
   - Search for "Apple" or "Tesla"
   - Click on a company to see details

2. **View Company Profile**
   - See risk score
   - Read executive summary
   - View recent news articles
   - Check sentiment analysis

3. **Create Watchlist**
   - Go to Watchlists
   - Create a new watchlist
   - Add companies to it

4. **Set Up Alerts**
   - Go to Alerts
   - Create a new alert
   - Choose alert type (risk increase, news, sentiment)

## API Examples

### Search Companies
```bash
curl "http://localhost:8000/api/search/companies?q=Apple"
```

### Get Company Profile
```bash
curl "http://localhost:8000/api/companies/{company_id}"
```

### Get Company Risk Score
```bash
curl "http://localhost:8000/api/companies/{company_id}/risk-score"
```

### Create Watchlist
```bash
curl -X POST "http://localhost:8000/api/watchlists/" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Watchlist", "description": "Test"}'
```

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Access Database
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U airi_user -d airi_db

# List tables
\dt

# Exit
\q
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Stop Services
```bash
docker-compose down
```

## Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache
docker-compose up -d
```

### Database connection error
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check database exists
docker-compose exec postgres psql -U airi_user -l
```

### Frontend not loading
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### API not responding
```bash
# Check backend logs
docker-compose logs backend

# Test health endpoint
curl http://localhost:8000/api/health
```

## Next Steps

1. **Explore the Code**
   - Backend: `backend/app/`
   - Frontend: `frontend/src/`

2. **Read Documentation**
   - Architecture: `ARCHITECTURE.md`
   - Deployment: `DEPLOYMENT.md`
   - Contributing: `CONTRIBUTING.md`

3. **Add Your Own Data**
   - Configure API keys in `.env`
   - Run ingestion: `docker-compose exec backend python scripts/load_sample_data.py`

4. **Customize**
   - Add new companies
   - Modify risk scoring rules
   - Customize dashboard

## Development

### Backend Development
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run linting
flake8 app tests
black app tests
```

### Frontend Development
```bash
# Install dependencies
cd frontend
npm install

# Run dev server
npm run dev

# Run tests
npm test
```

## Support

- Check logs: `docker-compose logs`
- Read README: `README.md`
- Check issues: GitHub Issues
- Review docs: `ARCHITECTURE.md`, `DEPLOYMENT.md`

## What's Next?

- [ ] Explore the dashboard
- [ ] Try the API endpoints
- [ ] Create watchlists
- [ ] Set up alerts
- [ ] Read the architecture docs
- [ ] Contribute improvements!

Happy exploring! 🚀

