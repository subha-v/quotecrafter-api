from datetime import datetime
from typing import Dict, List
from fastapi import APIRouter, HTTPException, status
from schemas.quote import (
    Quote, 
    QuoteCreate, 
    QuoteResponse, 
    QuoteListResponse,
    GenerateQuoteRequest
)
from services.ai_service import ai_service

# Router instance
router = APIRouter(prefix="/quotes", tags=["quotes"])

# In-memory storage
quotes_db: Dict[int, Quote] = {}
next_id = 1


def create_quote_record(quote_data: QuoteCreate) -> Quote:
    global next_id
    
    quote = Quote(
        id=next_id,
        author=quote_data.author,
        content=quote_data.content,
        created_at=datetime.utcnow()
    )
    
    quotes_db[next_id] = quote
    next_id += 1
    
    return quote


@router.post(
    "/", 
    response_model=QuoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new quote",
    description="Create a new quote with author and content"
)
async def create_quote(quote_data: QuoteCreate) -> QuoteResponse:
    try:
        quote = create_quote_record(quote_data)
        return QuoteResponse(
            success=True,
            data=quote,
            message="Quote created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create quote: {str(e)}"
        )


@router.get(
    "/",
    response_model=QuoteListResponse,
    summary="Get all quotes",
    description="Retrieve a list of all quotes"
)
async def list_quotes() -> QuoteListResponse:
    quotes_list = list(quotes_db.values())
    return QuoteListResponse(
        success=True,
        data=quotes_list,
        message="Quotes retrieved successfully",
        count=len(quotes_list)
    )


@router.get(
    "/{quote_id}",
    response_model=QuoteResponse,
    summary="Get quote by ID",
    description="Retrieve a specific quote by its ID"
)
async def get_quote(quote_id: int) -> QuoteResponse:
    if quote_id not in quotes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with ID {quote_id} not found"
        )
    
    quote = quotes_db[quote_id]
    return QuoteResponse(
        success=True,
        data=quote,
        message="Quote retrieved successfully"
    )


@router.post(
    "/generate",
    response_model=QuoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate AI quote",
    description="Generate a quote using AI based on a topic"
)
async def generate_quote(request: GenerateQuoteRequest) -> QuoteResponse:
    try:
        # Generate quote using AI service
        quote_content, quote_author = await ai_service.generate_quote(request.topic)
        
        # Create quote record in database
        quote_data = QuoteCreate(author=quote_author, content=quote_content)
        quote = create_quote_record(quote_data)
        
        return QuoteResponse(
            success=True,
            data=quote,
            message=f"Quote generated successfully for topic '{request.topic}'"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions from the AI service
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quote: {str(e)}"
        )


# Health check endpoint for the quotes service
@router.get(
    "/health",
    summary="Health check",
    description="Check if the quotes service is running"
)
async def health_check():
    return {
        "status": "healthy",
        "service": "quotes",
        "total_quotes": len(quotes_db),
        "ai_service_available": bool(ai_service.api_key)
    } 