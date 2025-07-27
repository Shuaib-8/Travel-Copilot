import pytest
from django.http import HttpResponse
from unittest.mock import patch
from core.llm_service import SYSTEM_MESSAGE


@pytest.mark.django_db
class TestTravelGuidanceView:
    """Test cases for the TravelGuidanceView class-based view."""
    
    @patch('travel_app.views.render')
    def test_get_request_renders_template(self, mock_render, client):
        """Test GET request renders the template with empty context."""
        mock_render.return_value = HttpResponse("Mocked template content")
    
        response = client.get('/')
        
        assert response.status_code == 200
        # Verify render was called with correct template and context
        mock_render.assert_called_once()
        # The actual request object will be created by Django, so we check call count
        assert len(mock_render.call_args_list) == 1
    
    @patch('travel_app.views.render')
    @patch('travel_app.views.get_travel_guidance')
    def test_post_request_with_valid_data(self, mock_service, mock_render, client):
        """Test POST request with valid travel guidance data."""
        mock_service.return_value = (
            "Here are some great places to visit in Tokyo: Shibuya, Senso-ji Temple, Tokyo Tower...",
            [
                {"role": "user", "content": "What are the best places to visit in Tokyo?"},
                {"role": "assistant", "content": "Here are some great places to visit in Tokyo..."}
            ]
        )
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Use client fixture for POST request
        response = client.post('/', {
            'user_message': 'What are the best places to visit in Tokyo?',
            'messages': []
        })
        
        assert response.status_code == 200
        # Verify service was called with correct parameters
        mock_service.assert_called_once_with('What are the best places to visit in Tokyo?', None)
        # Verify render was called
        mock_render.assert_called_once()

    @patch('travel_app.views.render')
    @patch('travel_app.views.get_travel_guidance')
    def test_post_request_with_conversation_history(self, mock_service, mock_render, client):
        """Test POST request with existing conversation history."""
        mock_service.return_value = (
            "Based on your interest in Tokyo, I also recommend visiting Kyoto for its temples.",
            [
                {"role": "system", "content": "You are a helpful assistant that provides information about travel destinations..."},
                {"role": "user", "content": "What are the best places to visit in Tokyo?"},
                {"role": "assistant", "content": "Here are some great places..."},
                {"role": "user", "content": "What about cultural sites?"},
                {"role": "assistant", "content": "Based on your interest in Tokyo..."}
            ]
        )
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Set up session with conversation history
        session = client.session
        session['conversation_history'] = [
            {
                'user_message': 'What are the best places to visit in Tokyo?',
                'ai_response': 'Here are some great places...'
            }
        ]
        session.save()
        
        response = client.post('/', {
            'user_message': 'What about cultural sites?'
        })
        
        assert response.status_code == 200
        
        # Verify service was called with proper message format including system message
        expected_messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": "What are the best places to visit in Tokyo?"},
            {"role": "assistant", "content": "Here are some great places..."}
        ]
        mock_service.assert_called_once_with('What about cultural sites?', expected_messages)
        mock_render.assert_called_once()
    
    @patch('travel_app.views.render')
    @patch('travel_app.views.get_travel_guidance')
    def test_post_request_empty_user_message(self, mock_service, mock_render, client):
        """Test POST request with empty user message."""
        mock_service.return_value = (
            "Please provide a question about travel.",
            [{"role": "assistant", "content": "Please provide a question about travel."}]
        )
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Use client fixture
        response = client.post('/', {
            'user_message': '',
            'messages': []
        })
        
        assert response.status_code == 200
        mock_service.assert_called_once_with('', None)
        mock_render.assert_called_once()
    