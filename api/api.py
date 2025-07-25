"""
Main API router for Django Ninja.
This file configures all API endpoints and routes.
"""

from typing import List, Optional
from ninja import NinjaAPI, Schema
from core import llm_service

# Define request schema for travel guidance
class TravelGuidanceRequest(Schema):
    user_message: str
    messages: Optional[List[dict]] = None

class TravelGuidanceResponse(Schema):
    response: str
    messages: List[dict]

# Create the main API instance
api = NinjaAPI(
    title="Travel Copilot API",
    version="1.0.0",
    description="API for travel planning co-pilot assistance"
)

# Register the travel guidance endpoint - singleton for LLM service
@api.post("/travel-guidance/", response=TravelGuidanceResponse)
def travel_guidance(request, data: TravelGuidanceRequest):
    """
    Endpoint to get travel guidance from the LLM service.
    
    Args:
        data: TravelGuidanceRequest containing user_message and optional messages history
        
    Returns:
        TravelGuidanceResponse: AI response and updated message history.
    """
    try:
        response, updated_messages = llm_service.get_travel_guidance(data.user_message, data.messages)
        return TravelGuidanceResponse(response=response, messages=updated_messages)
    except Exception as e:
        # Handle any unexpected errors
        error_response = f"An error occurred: {str(e)}"
        return TravelGuidanceResponse(
            response=error_response, 
            messages=[{"role": "system", "content": "Error occurred during processing"}]
        )

@api.get("/health-check/")
def health_check(request):
    """
    Simple health check endpoint to verify API is running.
    
    Returns:
        dict: Status message.
    """
    return {"status": "API is running smoothly!"}
