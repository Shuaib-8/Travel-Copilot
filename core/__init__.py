"""
Travel Copilot Core Module

This module contains the core business logic for the Travel Copilot application,
including LLM service integration with Cohere for travel guidance.
"""

from .llm_service import get_travel_guidance

__version__ = "0.1.0"
__all__ = ["get_travel_guidance"]
