# AIRI Deployment Guide

## Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Quick Start

```bash
# Clone repository
git clone <repo-url>
cd AIRI

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
# - OPENAI_API_KEY
# - NEWSAPI_KEY
# - SENDGRID_API_KEY (optional)

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python -m alembic upgrade head

# Load sample data
docker-compose exec backend python scripts/load_sample_data.py

# Access services
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Stopping Services

```bash
docker-compose down
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Production Deployment

### Docker Compose (Single Server)

```bash
# Build images
docker-compose -f docker-compose.yml build

# Start services
docker-compose -f docker-compose.yml up -d

# Run migrations
docker-compose exec backend python -m alembic upgrade head
```

### Kubernetes (Recommended for Scale)

#### Prerequisites
- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3+

#### Deployment

```bash
# Create namespace
kubectl create namespace airi

# Create secrets
kubectl create secret generic airi-secrets \
  --from-literal=openai-api-key=<key> \
  --from-literal=newsapi-key=<key> \
  --from-literal=sendgrid-api-key=<key> \
  -n airi

# Deploy using Helm (if available) or kubectl
kubectl apply -f k8s/ -n airi

# Check deployment
kubectl get pods -n airi
kubectl get svc -n airi
```

### Environment Variables

Key environment variables for production:

```
# Database
DATABASE_URL=postgresql://user:pass@host:5432/airi_db

# Redis
REDIS_URL=redis://host:6379/0

# Elasticsearch
ELASTICSEARCH_URL=http://host:9200

# LLM & Embeddings
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo

# Data Ingestion
NEWSAPI_KEY=...

# Email
SENDGRID_API_KEY=...

# Security
SECRET_KEY=<strong-random-key>
JWT_ALGORITHM=HS256

# Environment
ENVIRONMENT=production
DEBUG=false
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Monitoring & Logging

#### Application Logs
- Backend: `/var/log/airi/backend.log`
- Frontend: Browser console

#### Metrics
- Prometheus endpoint: `http://localhost:8000/metrics` (if enabled)
- Grafana dashboards for visualization

#### Health Checks
```bash
curl http://localhost:8000/api/health
```

### Backup & Recovery

#### Database Backup
```bash
# PostgreSQL backup
pg_dump -h localhost -U airi_user airi_db > backup.sql

# Restore
psql -h localhost -U airi_user airi_db < backup.sql
```

#### Elasticsearch Backup
```bash
# Create snapshot repository
curl -X PUT "localhost:9200/_snapshot/backup" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/mnt/backups"
  }
}'

# Create snapshot
curl -X PUT "localhost:9200/_snapshot/backup/snapshot_1"
```

### Scaling

#### Horizontal Scaling
- Run multiple backend instances behind a load balancer
- Use managed PostgreSQL for database
- Use managed Redis for caching
- Use managed Elasticsearch for search

#### Vertical Scaling
- Increase container resource limits
- Optimize database queries
- Enable caching strategies

### Security Checklist

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Use environment secrets (not in code)
- [ ] Enable database encryption
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] API rate limiting

### Troubleshooting

#### Database Connection Issues
```bash
# Check PostgreSQL
docker-compose exec postgres psql -U airi_user -d airi_db -c "SELECT 1"

# Check connection string
echo $DATABASE_URL
```

#### Elasticsearch Issues
```bash
# Check cluster health
curl http://localhost:9200/_cluster/health

# Check indices
curl http://localhost:9200/_cat/indices
```

#### API Issues
```bash
# Check logs
docker-compose logs backend

# Test endpoint
curl http://localhost:8000/api/health
```

## CI/CD Pipeline

The project includes GitHub Actions workflows for:
- Running tests on push/PR
- Building Docker images
- Code quality checks
- Coverage reporting

See `.github/workflows/ci.yml` for details.

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review documentation
3. Open GitHub issue with details

