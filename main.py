import logging
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import quotes

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting QuoteCrafter API...")
    logger.info(f"Debug mode: {os.getenv('DEBUG', 'False')}")
    logger.info(f"OpenRouter API configured: {bool(os.getenv('OPENROUTER_API_KEY'))}")
    yield
    # Shutdown
    logger.info("Shutting down QuoteCrafter API...")


# Create FastAPI application
app = FastAPI(
    title="QuoteCrafter API",
    version="1.0.0",
    description="""
    **QuoteCrafter** is a RESTful API service for managing quotes and generating inspirational quotes using AI.
    
    ## Features
    
    * **Quote Management**: Create, read, and list quotes
    * **AI Integration**: Generate inspirational quotes using OpenRouter AI models
    * **RESTful Design**: Clean, consistent API endpoints
    * **Auto Documentation**: Interactive API docs and schema
    
    ## Usage
    
    You can use this API to:
    * Store and retrieve inspirational quotes
    * Generate AI-powered quotes on any topic
    * Build quote-based applications and services
    
    ## Authentication
    
    No authentication required for basic quote operations. AI quote generation requires OpenRouter API configuration.
    """,
    contact={
        "name": "QuoteCrafter API",
        "url": "https://github.com/yourusername/quotecrafter",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quotes.router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to QuoteCrafter API!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "QuoteCrafter API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    ) 