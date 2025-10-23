# AIRI API Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently uses simplified authentication. In production, use JWT tokens:
```
Authorization: Bearer <token>
```

## Response Format
All responses are JSON:
```json
{
  "data": {},
  "error": null,
  "status": "success"
}
```

---

## Companies

### List Companies
```
GET /companies
```

**Query Parameters:**
- `skip` (int, default: 0) - Pagination offset
- `limit` (int, default: 10, max: 100) - Results per page

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Apple Inc.",
    "ticker": "AAPL",
    "industry": "Technology",
    "country": "US",
    "website": "https://apple.com",
    "description": "...",
    "risk_score": 25.5,
    "executive_summary": "...",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Create Company
```
POST /companies
```

**Request Body:**
```json
{
  "name": "Company Name",
  "ticker": "TICK",
  "industry": "Technology",
  "country": "US",
  "website": "https://example.com",
  "description": "Company description"
}
```

**Response:** Company object (201 Created)

### Get Company Profile
```
GET /companies/{company_id}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Apple Inc.",
  "ticker": "AAPL",
  "risk_score": 25.5,
  "executive_summary": "...",
  "recent_documents": [...],
  "sentiment_trend": {...},
  "risk_score_history": [...]
}
```

### Get Company Documents
```
GET /companies/{company_id}/documents
```

**Query Parameters:**
- `skip` (int, default: 0)
- `limit` (int, default: 20, max: 100)

**Response:**
```json
[
  {
    "id": "uuid",
    "company_id": "uuid",
    "title": "Article Title",
    "content": "Article content...",
    "source": "newsapi",
    "source_url": "https://...",
    "sentiment_score": 0.75,
    "sentiment_label": "positive",
    "entities": {"ORG": ["Apple"], "PERSON": ["Steve Jobs"]},
    "ingested_at": "2024-01-01T00:00:00"
  }
]
```

### Get Risk Score
```
GET /companies/{company_id}/risk-score
```

**Response:**
```json
{
  "company_id": "uuid",
  "risk_score": 25.5,
  "updated_at": "2024-01-01T00:00:00"
}
```

### Get Summary
```
GET /companies/{company_id}/summary
```

**Response:**
```json
{
  "company_id": "uuid",
  "summary": "Executive summary text...",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

## Search

### Search Companies
```
GET /search/companies
```

**Query Parameters:**
- `q` (string, required) - Search query
- `skip` (int, default: 0)
- `limit` (int, default: 10, max: 100)

**Response:**
```json
{
  "total": 5,
  "query": "Apple",
  "results": [...]
}
```

### Search Documents
```
GET /search/documents
```

**Query Parameters:**
- `q` (string, required) - Search query
- `skip` (int, default: 0)
- `limit` (int, default: 20, max: 100)

**Response:**
```json
{
  "total": 15,
  "query": "bankruptcy",
  "results": [...]
}
```

---

## Watchlists

### List Watchlists
```
GET /watchlists
```

**Response:**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "name": "My Watchlist",
    "description": "...",
    "items": [...],
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Create Watchlist
```
POST /watchlists
```

**Request Body:**
```json
{
  "name": "My Watchlist",
  "description": "Optional description"
}
```

**Response:** Watchlist object (201 Created)

### Get Watchlist
```
GET /watchlists/{watchlist_id}
```

**Response:** Watchlist object

### Add Company to Watchlist
```
POST /watchlists/{watchlist_id}/companies
```

**Request Body:**
```json
{
  "company_id": "uuid"
}
```

**Response:**
```json
{
  "message": "Company added to watchlist"
}
```

### Remove Company from Watchlist
```
DELETE /watchlists/{watchlist_id}/companies/{company_id}
```

**Response:**
```json
{
  "message": "Company removed from watchlist"
}
```

---

## Alerts

### List Alerts
```
GET /alerts
```

**Response:**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "email": "user@example.com",
    "alert_type": "risk_increase",
    "threshold": 70,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "last_triggered_at": null
  }
]
```

### Subscribe to Alerts
```
POST /alerts/subscribe
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "alert_type": "risk_increase",
  "watchlist_id": "uuid (optional)",
  "threshold": 70
}
```

**Alert Types:**
- `risk_increase` - Alert when risk score increases above threshold
- `news` - Alert on new news articles
- `sentiment` - Alert on sentiment changes

**Response:** Alert object (201 Created)

### Update Alert
```
PATCH /alerts/{alert_id}
```

**Request Body:**
```json
{
  "is_active": true
}
```

**Response:**
```json
{
  "message": "Alert updated"
}
```

### Delete Alert
```
DELETE /alerts/{alert_id}
```

**Response:**
```json
{
  "message": "Alert deleted"
}
```

---

## Health & Status

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "version": "0.1.0"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- API: 100 requests per minute per user
- NewsAPI: 100 requests per day (free tier)
- OpenAI: Based on account limits

---

## Pagination

All list endpoints support pagination:
- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 10-20, max: 100)

Example:
```
GET /companies?skip=20&limit=10
```

---

## Filtering & Sorting

### Search
Use the search endpoints for filtering:
```
GET /search/companies?q=Apple
GET /search/documents?q=bankruptcy
```

### Sorting
Results are sorted by:
- Companies: Name (alphabetical)
- Documents: Published date (newest first)
- Risk scores: Score (highest first)

---

## Examples

### Search for a company
```bash
curl "http://localhost:8000/api/search/companies?q=Apple"
```

### Get company profile
```bash
curl "http://localhost:8000/api/companies/{company_id}"
```

### Create watchlist
```bash
curl -X POST "http://localhost:8000/api/watchlists/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tech Companies", "description": "My tech watchlist"}'
```

### Subscribe to alerts
```bash
curl -X POST "http://localhost:8000/api/alerts/subscribe" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "alert_type": "risk_increase",
    "threshold": 70
  }'
```

---

## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

---

## Support

For API issues:
1. Check the error message
2. Review this reference
3. Check application logs
4. Open a GitHub issue

