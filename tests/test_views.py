import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from unittest.mock import patch, Mock
from travel_app.views import TravelGuidanceView

User = get_user_model()


@pytest.mark.django_db
class TestTravelGuidanceView:
    """Test cases for the TravelGuidanceView class-based view."""
    
    @patch('travel_app.views.render')
    def test_get_request_renders_template(self, mock_render, client):
        """Test GET request renders the template with empty context."""
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Use client fixture directly - much cleaner!
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
                {"role": "user", "content": "What are the best places to visit in Tokyo?"},
                {"role": "assistant", "content": "Here are some great places..."},
                {"role": "user", "content": "What about cultural sites?"},
                {"role": "assistant", "content": "Based on your interest in Tokyo..."}
            ]
        )
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # For Django forms, we need to send the JSON data as separate form fields
        # The view uses getlist() which expects multiple fields with the same name
        historical_messages = [
            '{"role": "user", "content": "What are the best places to visit in Tokyo?"}',
            '{"role": "assistant", "content": "Here are some great places..."}'
        ]
        
        response = client.post('/', {
            'user_message': 'What about cultural sites?',
            'messages': historical_messages  # This will be processed by getlist()
        })
        
        assert response.status_code == 200
        
        # Verify service was called with conversation history as a list of JSON strings
        mock_service.assert_called_once_with('What about cultural sites?', historical_messages)
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
    
    @patch('travel_app.views.render')
    @patch('travel_app.views.get_travel_guidance')
    def test_post_request_missing_user_message(self, mock_service, mock_render, client):
        """Test POST request without user_message field."""
        mock_service.return_value = (
            "Please provide a question about travel.",
            [{"role": "assistant", "content": "Please provide a question about travel."}]
        )
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Use client fixture
        response = client.post('/', {
            'messages': []
        })
        
        assert response.status_code == 200
        mock_service.assert_called_once_with('', None)
        mock_render.assert_called_once()
    
    @patch('travel_app.views.render')
    @patch('travel_app.views.get_travel_guidance')
    def test_post_request_service_error_handling(self, mock_service, mock_render, client):
        """Test POST request when service raises an exception."""
        mock_service.side_effect = Exception("Service unavailable")
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Use client fixture - this will handle the exception at the view level
        with pytest.raises(Exception, match="Service unavailable"):
            client.post('/', {
                'user_message': 'What are the best places to visit in Paris?',
                'messages': []
            })
    
    def test_view_template_name(self):
        """Test that the view uses the correct template."""
        view = TravelGuidanceView()
        assert view.template_name == 'travel_app/travel_guidance.html'
    
    @patch('travel_app.views.render')
    @patch('travel_app.views.get_travel_guidance')
    def test_post_request_with_special_characters(self, mock_service, mock_render, client):
        """Test POST request with special characters and emojis."""
        mock_service.return_value = (
            "São Paulo is a vibrant city with amazing cuisine! 🇧🇷",
            [
                {"role": "user", "content": "Tell me about São Paulo's café culture! ☕"},
                {"role": "assistant", "content": "São Paulo is a vibrant city with amazing cuisine! 🇧🇷"}
            ]
        )
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Use client fixture
        response = client.post('/', {
            'user_message': "Tell me about São Paulo's café culture! ☕",
            'messages': []
        })
        
        assert response.status_code == 200
        # Verify the service was called with special characters preserved
        mock_service.assert_called_once_with("Tell me about São Paulo's café culture! ☕", None)
        mock_render.assert_called_once()
    
    @patch('travel_app.views.render')
    @patch('travel_app.views.get_travel_guidance')
    def test_post_request_long_message(self, mock_service, mock_render, client):
        """Test POST request with very long user message."""
        long_message = "Tell me about travel " * 100  # Very long message
        mock_service.return_value = (
            "Here's comprehensive travel information...",
            [
                {"role": "user", "content": long_message},
                {"role": "assistant", "content": "Here's comprehensive travel information..."}
            ]
        )
        mock_render.return_value = HttpResponse("Mocked template content")
        
        # Use client fixture
        response = client.post('/', {
            'user_message': long_message,
            'messages': []
        })
        
        assert response.status_code == 200
        mock_service.assert_called_once_with(long_message, None)
        mock_render.assert_called_once()
