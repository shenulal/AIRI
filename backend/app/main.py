"""FastAPI application entry point."""
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db, engine
from app.models import Base
from app.schemas import HealthResponse
from app.api import companies, watchlists, alerts, search

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    print("Starting AIRI application...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified")
    
    yield
    
    # Shutdown
    print("Shutting down AIRI application...")


# Create FastAPI app
app = FastAPI(
    title="AIRI - AI Insights & Risk Intelligence Platform",
    description="API for company intelligence, risk scoring, and sentiment analysis",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(watchlists.router, prefix="/api/watchlists", tags=["watchlists"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(search.router, prefix="/api/search", tags=["search"])


@app.get("/api/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """Health check endpoint."""
    try:
        # Test database connection
        db.execute("SELECT 1")
        status = "healthy"
    except Exception as e:
        print(f"Health check failed: {e}")
        status = "unhealthy"
    
    return HealthResponse(
        status=status,
        timestamp=datetime.utcnow(),
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AIRI - AI Insights & Risk Intelligence Platform",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
    )

