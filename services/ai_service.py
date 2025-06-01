import asyncio
import logging
import os
from typing import Optional
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

logger = logging.getLogger(__name__)


class OpenRouterService:
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout = 30.0
        self.max_retries = 3
        self.model = "openai/gpt-3.5-turbo"  # Free tier model
        
        if not self.api_key:
            logger.warning("OpenRouter API key not found. AI quote generation will not work.")
    
    async def generate_quote(self, topic: str) -> tuple[str, str]:
        if not self.api_key:
            raise HTTPException(
                status_code=503, 
                detail="AI quote generation is not available. OpenRouter API key not configured."
            )
        
        prompt = self._create_prompt(topic)
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "temperature": 0.7,
                            "max_tokens": 150
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return self._parse_response(data, topic)
                    elif response.status_code == 429:
                        # Rate limited, wait and retry
                        if attempt < self.max_retries - 1:
                            wait_time = 2 ** attempt
                            logger.warning(f"Rate limited, waiting {wait_time}s before retry {attempt + 1}")
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
                    else:
                        logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(1)
                            continue
                        else:
                            raise HTTPException(
                                status_code=502, 
                                detail="Failed to generate quote. External AI service unavailable."
                            )
                            
            except httpx.TimeoutException:
                logger.error(f"Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                else:
                    raise HTTPException(status_code=504, detail="Request timeout. Please try again.")
            except httpx.RequestError as e:
                logger.error(f"Request error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                else:
                    raise HTTPException(status_code=502, detail="Failed to connect to AI service.")
        
        raise HTTPException(status_code=502, detail="Failed to generate quote after multiple attempts.")
    
    def _create_prompt(self, topic: str) -> str:
        return f"""Generate an inspirational quote about "{topic}". 
        
Please respond with ONLY the following format:
Quote: [Your quote here]
Author: [Author name or "Anonymous"]

The quote should be meaningful, inspiring, and relevant to the topic "{topic}". Make it concise but impactful."""
    
    def _parse_response(self, data: dict, topic: str) -> tuple[str, str]:
        try:
            content = data["choices"][0]["message"]["content"].strip()
            
            # Try to parse the structured response
            lines = content.split('\n')
            quote_content = None
            author = None
            
            for line in lines:
                line = line.strip()
                if line.startswith("Quote:"):
                    quote_content = line.replace("Quote:", "").strip().strip('"')
                elif line.startswith("Author:"):
                    author = line.replace("Author:", "").strip()
            
            # Fallback parsing if structured format not found
            if not quote_content:
                # Look for content in quotes or use the whole response
                if '"' in content:
                    start = content.find('"')
                    end = content.rfind('"')
                    if start != end and start != -1:
                        quote_content = content[start+1:end]
                        # Try to find author after the quote
                        remaining = content[end+1:].strip()
                        if remaining and not remaining.startswith('-'):
                            author = remaining.lstrip('- ').strip()
                else:
                    quote_content = content
            
            # Set defaults if parsing failed
            if not quote_content:
                quote_content = f"Every moment is a fresh beginning."
            if not author:
                author = "Anonymous"
                
            return quote_content, author
            
        except (KeyError, IndexError, AttributeError) as e:
            logger.error(f"Failed to parse OpenRouter response: {e}")
            # Return a fallback quote
            return f"Every challenge in {topic} is an opportunity in disguise.", "Anonymous"


# Global service instance
ai_service = OpenRouterService() 