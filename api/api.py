"""
Main API router for Django Ninja.
This file configures all API endpoints and routes.
"""

from ninja import NinjaAPI

# Create the main API instance
api = NinjaAPI(
    title="Travel Copilot API",
    version="1.0.0",
    description="API for travel planning co-pilot assistance",
)

