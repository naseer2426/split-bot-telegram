import os
import logging
from typing import Optional
import httpx

logger = logging.getLogger(__name__)

class SplitBotRequest:
    def __init__(self, message: str, group_id: str, sender: str, image_url: Optional[str] = None):
        self.message = message
        self.group_id = group_id
        self.sender = sender
        self.image_url = image_url

    def to_dict(self) -> dict:
        """Convert SplitBotRequest to dictionary for JSON serialization."""
        result = {
            "message": self.message,
            "group_id": self.group_id,
            "sender": self.sender
        }
        if self.image_url is not None:
            result["image_url"] = self.image_url
        return result


async def process_message(request: SplitBotRequest) -> str:
    # Read SPLIT_BOT_URL from environment variables
    SPLIT_BOT_URL = os.getenv("SPLIT_BOT_URL")
    if not SPLIT_BOT_URL:
        raise ValueError("SPLIT_BOT_URL not found in environment variables")
        
    url = f"{SPLIT_BOT_URL}/process_message"
    request_body = request.to_dict()
    
    # Log request
    logger.info(f"Making POST request to {url}")
    logger.info(f"Request body: {request_body}")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url,
            json=request_body
        )
        
        # Log response
        logger.info(f"Response status code: {response.status_code}")
        response_data = response.json()
        logger.info(f"Response body: {response_data}")
        
        # Check status code
        if response.status_code != 200:
            raise ValueError(f"Request failed with status code {response.status_code}")
        
        # Check error field - treat None/null the same as empty string
        error = response_data.get("error") or ""
        if error != "":
            raise ValueError(f"Error in response: {error}")
        
        # Return the response string
        return response_data.get("response", "")
