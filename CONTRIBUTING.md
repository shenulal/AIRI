# Contributing to AIRI

Thank you for your interest in contributing to AIRI! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Setup Development Environment

```bash
# Clone repository
git clone <repo-url>
cd AIRI

# Create feature branch
git checkout -b feature/your-feature-name

# Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend
cd ../frontend
npm install

# Start development environment
cd ..
docker-compose up -d
```

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/descriptive-name
# or
git checkout -b fix/issue-number
```

### 2. Make Changes
- Write clean, readable code
- Follow project conventions
- Add docstrings and comments
- Keep commits atomic and descriptive

### 3. Write Tests
```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

### 4. Run Linting
```bash
# Backend
cd backend
flake8 app tests
black app tests
isort app tests

# Frontend
cd frontend
npm run lint
```

### 5. Commit Changes
```bash
git add .
git commit -m "feat: add new feature" -m "Detailed description of changes"
```

### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title
- Description of changes
- Related issues
- Screenshots (if UI changes)

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Max line length: 100
- Use docstrings for functions/classes

Example:
```python
def calculate_risk_score(
    company_id: str, 
    db: Session
) -> float:
    """Calculate composite risk score for a company.
    
    Args:
        company_id: Company identifier
        db: Database session
        
    Returns:
        Risk score between 0 and 100
    """
    # Implementation
    pass
```

### TypeScript/React
- Use TypeScript for type safety
- Follow ESLint rules
- Use functional components
- Add prop types

Example:
```typescript
interface CompanyProps {
  id: string
  name: string
  riskScore: number
}

export function CompanyCard({ id, name, riskScore }: CompanyProps) {
  return (
    <div>
      <h3>{name}</h3>
      <p>Risk: {riskScore}</p>
    </div>
  )
}
```

## Testing Guidelines

### Backend Tests
- Unit tests for services
- Integration tests for API
- Test database interactions
- Mock external APIs

```bash
# Run tests with coverage
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests
- Component tests
- Integration tests
- User interaction tests

```bash
# Run tests
npm test

# With coverage
npm test -- --coverage
```

### Test Coverage
- Target: 80%+ coverage
- All public functions tested
- Edge cases covered
- Error scenarios tested

## Documentation

### Code Documentation
- Add docstrings to all functions
- Document complex logic
- Include examples where helpful
- Update README for new features

### API Documentation
- Document new endpoints
- Include request/response examples
- Add error codes
- Update Swagger/OpenAPI

### User Documentation
- Update README
- Add setup instructions
- Document new features
- Include troubleshooting

## Adding New Data Sources

### Steps to Add a New Ingestion Source

1. **Create Ingester Class**
```python
# backend/app/services/ingestion_service.py

class NewSourceIngester:
    def __init__(self):
        self.api_key = settings.new_source_api_key
    
    def ingest_company_data(self, db: Session, company_name: str):
        # Implementation
        pass
```

2. **Add to IngestionService**
```python
class IngestionService:
    def __init__(self):
        self.new_source = NewSourceIngester()
    
    def ingest_company(self, db: Session, company_name: str):
        # Call new source
        pass
```

3. **Add Configuration**
```python
# backend/app/config.py
new_source_api_key: Optional[str] = None
```

4. **Update .env.example**
```
NEW_SOURCE_API_KEY=your_api_key
```

5. **Add Tests**
```python
# backend/tests/test_ingestion.py
def test_new_source_ingester(db):
    # Test implementation
    pass
```

6. **Document**
- Update README
- Add to ARCHITECTURE.md
- Document API keys needed

## Pull Request Process

1. **Before Submitting**
   - [ ] Tests pass locally
   - [ ] Code is linted
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)

2. **PR Description**
   - Clear title
   - Description of changes
   - Related issues (#123)
   - Screenshots (if applicable)

3. **Review Process**
   - At least 1 approval required
   - CI/CD pipeline must pass
   - Address review comments
   - Squash commits if requested

4. **Merging**
   - Rebase on main
   - Delete feature branch
   - Close related issues

## Reporting Issues

### Bug Reports
Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Error logs/screenshots

### Feature Requests
Include:
- Clear description
- Use case/motivation
- Proposed solution (if any)
- Alternative solutions

## Performance Considerations

- Optimize database queries
- Use caching appropriately
- Minimize API calls
- Profile before optimizing
- Document performance implications

## Security

- Never commit secrets
- Use environment variables
- Validate all inputs
- Sanitize outputs
- Report security issues privately

## Questions?

- Check existing issues/discussions
- Review documentation
- Ask in pull request comments
- Open a discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to AIRI! 🚀

