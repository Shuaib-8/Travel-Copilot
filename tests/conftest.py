import pytest
import os
from unittest.mock import Mock, patch
from django.test import Client
from django.contrib.auth import get_user_model
from django.conf import settings
from core.llm_service import SYSTEM_MESSAGE


@pytest.fixture
def sample_travel_request_with_history():
    """Sample travel guidance request with conversation history."""
    return {
        'user_message': 'What about restaurants?',
        'messages': [
            {'role': 'system', 'content': SYSTEM_MESSAGE},
            {'role': 'user', 'content': 'What are the best places to visit in Paris?'},
            {'role': 'assistant', 'content': 'Paris has many attractions like the Eiffel Tower...'}
        ]
    }


@pytest.fixture
def sample_llm_response():
    """Sample LLM response for testing."""
    return (
        "Here are some great places to visit in Paris: Eiffel Tower, Louvre Museum, Notre-Dame Cathedral...",
        [
            {'role': 'system', 'content': SYSTEM_MESSAGE},
            {'role': 'user', 'content': 'What are the best places to visit in Paris?'},
            {'role': 'assistant', 'content': 'Here are some great places to visit in Paris: Eiffel Tower, Louvre Museum, Notre-Dame Cathedral...'}
        ]
    )


@pytest.fixture
def mock_llm_service_success(sample_llm_response):
    """Mock LLM service to return successful response."""
    # Patch at both locations - the core module and the API module that imports it
    with patch('core.llm_service.get_travel_guidance') as mock_service1, \
         patch('api.api.get_travel_guidance') as mock_service2:
        
        response_data = sample_llm_response
        mock_service1.return_value = response_data
        mock_service2.return_value = response_data
        
        # Return the API-level mock since that's what the API tests will check
        yield mock_service2
