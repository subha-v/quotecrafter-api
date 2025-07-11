from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class QuoteCreate(BaseModel):
    author: str = Field(..., min_length=1, max_length=255, description="The author of the quote")
    content: str = Field(..., min_length=1, max_length=2000, description="The quote content")


class Quote(BaseModel):
    id: int = Field(..., description="Unique identifier for the quote")
    author: str = Field(..., description="The author of the quote")
    content: str = Field(..., description="The quote content")
    created_at: datetime = Field(..., description="When the quote was created")


class QuoteResponse(BaseModel):
    success: bool = Field(True, description="Whether the operation was successful")
    data: Quote = Field(..., description="The quote data")
    message: str = Field("Success", description="Response message")


class QuoteListResponse(BaseModel):
    success: bool = Field(True, description="Whether the operation was successful")
    data: List[Quote] = Field(..., description="List of quotes")
    message: str = Field("Success", description="Response message")
    count: int = Field(..., description="Number of quotes returned")


class GenerateQuoteRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=255, description="Topic for quote generation") 