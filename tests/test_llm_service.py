import pytest
from unittest.mock import patch, Mock
from core.llm_service import get_travel_guidance, SYSTEM_MESSAGE


class TestGetTravelGuidance:
    """Test the main get_travel_guidance function."""
    
    @patch('core.llm_service.co_v2')
    def test_get_travel_guidance_new_conversation(self, mock_client):
        """Test travel guidance with new conversation (no history)."""
        # Mock the Cohere response
        mock_response = Mock()
        mock_response.message.content = [
            Mock(text="Paris is a beautiful city with many attractions like the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral.")
        ]
        mock_client.chat.return_value = mock_response
        
        user_message = "What are the best places to visit in Paris?"
        response, messages = get_travel_guidance(user_message)
        
        # Verify response
        assert "Paris" in response
        assert "Eiffel Tower" in response
        
        # Verify messages structure (returned by function)
        assert len(messages) == 3  # system + user + assistant
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == SYSTEM_MESSAGE
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == user_message
        assert messages[2]["role"] == "assistant"
        assert messages[2]["content"] == response

        # Verify the chat was called once
        mock_client.chat.assert_called_once()
    
    @patch('core.llm_service.co_v2')
    def test_get_travel_guidance_with_history(self, mock_client):
        """Test travel guidance with existing conversation history."""
        # Mock the Cohere response
        mock_response = Mock()
        mock_response.message.content = [
            Mock(text="For restaurants in Paris, I recommend Le Comptoir du Relais, L'As du Fallafel, and Breizh Café.")
        ]
        
        # Capture the call arguments at the time of the call
        api_call_messages = []
        def capture_call(*args, **kwargs):
            api_call_messages.extend(kwargs['messages'].copy())  # Capture a copy
            return mock_response
        
        mock_client.chat.side_effect = capture_call
        
        user_message = "What about restaurants?"
        existing_messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": "What are the best places to visit in Paris?"},
            {"role": "assistant", "content": "Paris has many attractions like the Eiffel Tower..."}
        ]
        
        response, messages = get_travel_guidance(user_message, existing_messages)
        
        # Verify response
        assert "restaurant" in response.lower()
        assert "Paris" in response
        
        # Verify messages structure (returned by function)
        assert len(messages) == 5  # original 3 + user + assistant
        assert messages[-2]["role"] == "user"
        assert messages[-2]["content"] == user_message
        assert messages[-1]["role"] == "assistant"
        assert messages[-1]["content"] == response
        
        # Verify API call - messages sent to API should be original 3 + new user message
        assert len(api_call_messages) == 4  # original 3 + new user message
        assert api_call_messages[-1]["role"] == "user"  # Last message should be the new user message
        assert api_call_messages[-1]["content"] == user_message
        
        # Verify the chat was called once
        mock_client.chat.assert_called_once()
    
    @patch('core.llm_service.co_v2')
    def test_get_travel_guidance_api_error(self, mock_client):
        """Test travel guidance when API returns an error."""
        # Mock API to raise an exception
        mock_client.chat.side_effect = Exception("API Error: Rate limit exceeded")
        
        user_message = "What are the best places to visit in Tokyo?"
        
        # The service handles exceptions and returns error messages
        response, messages = get_travel_guidance(user_message)
        
        # Verify error is handled gracefully
        assert "Error getting travel guidance" in response
        assert "API Error: Rate limit exceeded" in response
        assert len(messages) == 1  # Only system message returned on error
        assert messages[0]["role"] == "system"
    
    @patch('core.llm_service.co_v2')
    def test_get_travel_guidance_empty_message(self, mock_client):
        """Test travel guidance with empty user message."""
        mock_response = Mock()
        mock_response.message.content = [
            Mock(text="Please provide a specific question about travel destinations or planning.")
        ]
        mock_client.chat.return_value = mock_response
        
        user_message = ""
        response, messages = get_travel_guidance(user_message)
        
        # Should still process the request
        assert len(messages) == 3
        assert messages[1]["content"] == ""  # Empty user message preserved
        mock_client.chat.assert_called_once()
    
    @patch('core.llm_service.co_v2')
    def test_get_travel_guidance_long_conversation(self, mock_client):
        """Test travel guidance with long conversation history."""
        mock_response = Mock()
        mock_response.message.content = [
            Mock(text="Based on our previous discussion about Japan, I'd recommend visiting in spring for cherry blossoms.")
        ]
        mock_client.chat.return_value = mock_response
        
        # Create a long conversation history
        long_history = [{"role": "system", "content": SYSTEM_MESSAGE}]
        for i in range(10):
            long_history.extend([
                {"role": "user", "content": f"Question {i}"},
                {"role": "assistant", "content": f"Answer {i}"}
            ])
        
        user_message = "When is the best time to visit Japan?"
        response, messages = get_travel_guidance(user_message, long_history)
        
        # Verify conversation continues properly
        assert len(messages) == len(long_history) + 2  # +2 for new user + assistant
        assert "spring" in response.lower()
        mock_client.chat.assert_called_once()
