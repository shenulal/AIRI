# AIRI 8-Week Sprint Plan

## Overview
This document outlines the 8-week development plan for AIRI MVP, with clear milestones and deliverables.

## Sprint 1-2: Foundation & Core Infrastructure (Weeks 1-2)

### Goals
- Set up project structure and development environment
- Implement database schema and migrations
- Create basic API endpoints

### Tasks
- [x] Project scaffolding and Docker setup
- [x] PostgreSQL schema design and migrations
- [x] FastAPI application structure
- [x] Basic CRUD endpoints for companies
- [x] React project setup with Vite

### Deliverables
- Working Docker Compose environment
- Database with all tables
- Basic API endpoints
- Frontend scaffolding

### Success Criteria
- `docker-compose up` starts all services
- Database migrations run successfully
- API endpoints respond correctly
- Frontend builds without errors

---

## Sprint 3-4: Data Ingestion & NLP (Weeks 3-4)

### Goals
- Implement data ingestion from NewsAPI and OpenCorporates
- Build NLP pipeline for sentiment and NER
- Create embeddings service

### Tasks
- [ ] NewsAPI ingestion service
- [ ] OpenCorporates ingestion service
- [ ] Data normalization pipeline
- [ ] Sentiment analysis implementation
- [ ] Named Entity Recognition (NER)
- [ ] Embeddings generation service
- [ ] Elasticsearch indexing

### Deliverables
- Working ingestion for 2+ sources
- NLP pipeline processing documents
- Embeddings stored in vector DB
- Full-text search via Elasticsearch

### Success Criteria
- Ingest 100+ documents from NewsAPI
- Sentiment scores computed for all documents
- Embeddings generated and stored
- Search returns relevant results

---

## Sprint 5: Risk Scoring & RAG (Weeks 5)

### Goals
- Implement risk scoring engine
- Build RAG pipeline for summaries
- Create company profile endpoints

### Tasks
- [ ] Rule-based risk scoring
- [ ] ML-based risk scoring (logistic regression)
- [ ] Risk score aggregation
- [ ] RAG pipeline implementation
- [ ] LLM summary generation
- [ ] Company profile endpoint

### Deliverables
- Risk scores for all companies
- Executive summaries via LLM
- Company profile API endpoint
- Risk score history tracking

### Success Criteria
- Risk scores between 0-100
- Summaries generated for 10+ companies
- Profile endpoint returns all data
- Risk scores update on new documents

---

## Sprint 6: API & Watchlists (Week 6)

### Goals
- Complete REST API implementation
- Implement watchlists and alerts
- Add search functionality

### Tasks
- [ ] Search endpoints (companies, documents)
- [ ] Watchlist CRUD operations
- [ ] Alert subscription system
- [ ] Email alert integration (SendGrid)
- [ ] API documentation (Swagger)
- [ ] Request validation and error handling

### Deliverables
- Complete REST API
- Watchlist management
- Alert system with email
- API documentation

### Success Criteria
- All endpoints documented in Swagger
- Watchlists can be created and managed
- Alerts trigger on risk changes
- Email alerts sent successfully

---

## Sprint 7: Frontend Dashboard (Week 7)

### Goals
- Build React dashboard UI
- Implement all frontend pages
- Connect to backend API

### Tasks
- [ ] Search page implementation
- [ ] Company profile page
- [ ] Watchlist management UI
- [ ] Alert configuration UI
- [ ] Sentiment timeline visualization
- [ ] Responsive design
- [ ] Error handling and loading states

### Deliverables
- Fully functional React dashboard
- All pages implemented
- API integration complete
- Responsive design

### Success Criteria
- Dashboard loads without errors
- Search works end-to-end
- Company profiles display correctly
- Watchlists can be managed
- Mobile responsive

---

## Sprint 8: Testing, CI/CD & Documentation (Week 8)

### Goals
- Comprehensive testing
- CI/CD pipeline setup
- Complete documentation

### Tasks
- [ ] Unit tests for services
- [ ] Integration tests for API
- [ ] Frontend component tests
- [ ] GitHub Actions CI/CD setup
- [ ] Docker image optimization
- [ ] README and setup guides
- [ ] Architecture documentation
- [ ] Deployment guides

### Deliverables
- 80%+ code coverage
- Passing CI/CD pipeline
- Complete documentation
- Deployment ready

### Success Criteria
- All tests passing
- CI/CD pipeline green
- README complete
- Can deploy to production

---

## Milestone Summary

| Milestone | Week | Status |
|-----------|------|--------|
| MVP Foundation | 2 | ✓ Complete |
| Data Ingestion | 4 | In Progress |
| Risk & RAG | 5 | Planned |
| API Complete | 6 | Planned |
| Dashboard | 7 | Planned |
| Production Ready | 8 | Planned |

---

## Key Metrics

### Code Quality
- Target: 80%+ test coverage
- Target: 0 critical security issues
- Target: <5 code smells per 1000 LOC

### Performance
- API response time: <500ms (p95)
- Search latency: <1s
- Dashboard load time: <3s

### Reliability
- Uptime: 99.5%
- Error rate: <0.1%
- Data consistency: 100%

---

## Risk Mitigation

### Technical Risks
- **API Rate Limits**: Implement caching and rate limiting
- **LLM Costs**: Cache embeddings, batch requests
- **Database Performance**: Add indices, optimize queries

### Resource Risks
- **API Key Availability**: Use free tier limits, implement fallbacks
- **Infrastructure**: Use managed services for scalability

### Schedule Risks
- **Scope Creep**: Focus on MVP features only
- **Integration Issues**: Early integration testing

---

## Post-MVP Roadmap

### Phase 2 (Weeks 9-12)
- Advanced ML models
- Real-time updates (WebSocket)
- Multi-user authentication
- Advanced search features

### Phase 3 (Weeks 13-16)
- Kubernetes deployment
- Horizontal scaling
- Advanced analytics
- Third-party integrations

### Phase 4 (Weeks 17+)
- Mobile app
- Advanced compliance features
- Custom ML models
- Enterprise features

---

## Team Responsibilities

### Backend
- Data ingestion
- NLP pipeline
- Risk scoring
- API implementation
- Database management

### Frontend
- UI/UX design
- React components
- API integration
- Testing

### DevOps
- Docker setup
- CI/CD pipeline
- Deployment
- Monitoring

---

## Communication & Standup

- **Daily Standup**: 15 min (async or sync)
- **Sprint Review**: End of week
- **Sprint Planning**: Start of week
- **Retrospective**: End of sprint

---

## Success Criteria for MVP

✓ Data ingestion from 2+ sources
✓ NLP pipeline (sentiment, NER)
✓ Risk scoring (rule + ML)
✓ RAG-based summaries
✓ REST API with 20+ endpoints
✓ React dashboard
✓ Watchlists and alerts
✓ 80%+ test coverage
✓ CI/CD pipeline
✓ Complete documentation
✓ Deployable to production

