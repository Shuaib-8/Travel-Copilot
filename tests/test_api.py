import pytest
import json
from unittest.mock import patch, Mock

# Import after Django setup to avoid settings errors
from api.api import api, TravelGuidanceRequest, TravelGuidanceResponse 


@pytest.mark.django_db
class TestTravelGuidanceAPI:
    """Test cases for the travel guidance API endpoint."""
    
    def test_travel_guidance_request_schema(self):
        """Test TravelGuidanceRequest schema validation."""
        # Valid request with minimal data
        valid_data = {"user_message": "What are the best places to visit in Paris?"}
        request = TravelGuidanceRequest(**valid_data)
        assert request.user_message == "What are the best places to visit in Paris?"
        assert request.messages is None
        
        # Valid request with messages history
        valid_data_with_messages = {
            "user_message": "What about restaurants?",
            "messages": [
                {"role": "user", "content": "Tell me about Paris"},
                {"role": "assistant", "content": "Paris is beautiful..."}
            ]
        }
        request_with_messages = TravelGuidanceRequest(**valid_data_with_messages)
        assert request_with_messages.user_message == "What about restaurants?"
        assert len(request_with_messages.messages) == 2
    
    def test_travel_guidance_response_schema(self):
        """Test TravelGuidanceResponse schema validation."""
        response_data = {
            "response": "Here are some great places to visit in Paris...",
            "messages": [
                {"role": "user", "content": "Tell me about Paris"},
                {"role": "assistant", "content": "Here are some great places..."}
            ]
        }
        response = TravelGuidanceResponse(**response_data)
        assert response.response == "Here are some great places to visit in Paris..."
        assert len(response.messages) == 2
    
    def test_travel_guidance_endpoint_success(self, client, mock_llm_service_success):
        """Test successful travel guidance endpoint call."""
        request_data = {
            "user_message": "What are the best places to visit in Paris?",
            "messages": None
        }
        
        response = client.post(
            "/api/travel-guidance/", 
            data=json.dumps(request_data),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert "messages" in response_data
        assert response_data["response"] == "Here are some great places to visit in Paris: Eiffel Tower, Louvre Museum, Notre-Dame Cathedral..."
        assert len(response_data["messages"]) == 3  # system + user + assistant
    
    
    def test_travel_guidance_endpoint_invalid_json(self, client):
        """Test travel guidance endpoint with invalid JSON."""
        # Missing required field
        invalid_data = {"messages": None}  # Missing user_message
        
        response = client.post(
            "/api/travel-guidance/", 
            data=json.dumps(invalid_data),
            content_type="application/json"
        )
        
        assert response.status_code == 422  # Validation error
    

    def test_health_check_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/health-check/")
        
        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data
        assert "API is running smoothly!" in response_data["status"]
    
    
    def test_api_configuration(self):
        """Test API configuration and metadata."""
        assert api.title == "Travel Copilot API"
        assert api.version == "1.0.0"
        assert "travel planning" in api.description.lower()


    def test_travel_guidance_endpoint_with_history(self, client, sample_travel_request_with_history, mock_llm_service_success):
        """Test travel guidance endpoint with conversation history."""
        
        response = client.post(
            "/api/travel-guidance/", 
            data=json.dumps(sample_travel_request_with_history),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert "messages" in response_data
        assert response_data["response"] == "Here are some great places to visit in Paris: Eiffel Tower, Louvre Museum, Notre-Dame Cathedral..."
        assert len(response_data["messages"]) == 3  # system + user + assistant
        
        # Verify the mock was called with the correct parameters
        mock_llm_service_success.assert_called_once_with(
            sample_travel_request_with_history["user_message"], # 'What about restaurants?'
            sample_travel_request_with_history["messages"]
        )

        assert mock_llm_service_success.call_count == 1
        # Check the response messages structure
        messages = response_data["messages"]
        assert len(messages) == 3
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[2]["role"] == "assistant"
    

    def test_travel_guidance_endpoint_empty_message(self, client, mock_llm_service_success):
        """Test travel guidance endpoint with empty message."""
        request_data = {
            "user_message": "",
            "messages": None
        }
        
        response = client.post(
            "/api/travel-guidance/", 
            data=json.dumps(request_data),
            content_type="application/json"
        )
        
        # Should either return 422 for validation error or handle gracefully
        assert response.status_code in [200, 422]

        # If the request was successful (status 200), verify the mock was called
        if response.status_code == 200:
            mock_llm_service_success.assert_called_once_with("", None)
        # If the request was unsuccessful (status 422), check the error message
        if response.status_code == 422:
            response_data = response.json()
            assert "detail" in response_data
            assert "user_message" in response_data["detail"][0]["loc"]
            assert "This field may not be blank." in response_data["detail"][0]["msg"]
    

    def test_travel_guidance_endpoint_integration(self, client, mock_llm_service_success):
        """Test travel guidance endpoint integration with mocked service."""
        request_data = {
            "user_message": "Plan a 3-day trip to Rome",
            "messages": None
        }
        
        response = client.post(
            "/api/travel-guidance/", 
            data=json.dumps(request_data),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert "messages" in response_data
        assert len(response_data["messages"]) == 3  # system + user + assistant
        
        # Verify the mock was called
        mock_llm_service_success.assert_called_once_with("Plan a 3-day trip to Rome", None)


@pytest.mark.django_db
class TestAPISchemas:
    """Test API schema validation."""
    
    def test_travel_guidance_request_validation(self):
        """Test TravelGuidanceRequest schema validation."""
        # Valid request
        valid_data = {"user_message": "Test message"}
        request = TravelGuidanceRequest(**valid_data)
        assert request.user_message == "Test message"
        assert request.messages is None
        
        # Request with messages
        data_with_messages = {
            "user_message": "Test message",
            "messages": [{"role": "user", "content": "Hello"}]
        }
        request_with_msgs = TravelGuidanceRequest(**data_with_messages)
        assert len(request_with_msgs.messages) == 1
    
    def test_travel_guidance_response_validation(self):
        """Test TravelGuidanceResponse schema validation."""
        response_data = {
            "response": "Test response",
            "messages": [
                {"role": "user", "content": "Test"},
                {"role": "assistant", "content": "Test response"}
            ]
        }
        response = TravelGuidanceResponse(**response_data)
        assert response.response == "Test response"
        assert len(response.messages) == 2
