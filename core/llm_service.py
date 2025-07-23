import os
from dotenv import load_dotenv
from cohere import ClientV2
from pathlib import Path

# Load environment variables from .env file (local development)
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

COHERE_API_KEY = os.getenv('COHERE_API_KEY')

SYSTEM_MESSAGE = """
You are a helpful assistant that provides information about travel destinations, 
including popular attractions, local cuisine, and cultural experiences.
You can also assist with travel planning, such as suggesting itineraries and
providing tips for travelers. 
Anything outside your domain expertise of travel including illegal activities 
or banned items in certain destinations while travelling, please decline to respond. 
"""

# Initialize the Cohere client
co_v2 = ClientV2(api_key=COHERE_API_KEY)

def get_travel_guidance(user_message: str, messages: list = None) -> tuple[str, list]:
    """
    Get travel guidance from Cohere API using the system message.
    It will refuse to answer questions outside the travel domain.
    Supports multi-turn conversations through message history.
    
    Args:
        user_message (str): The user's question about travel
        messages (list, optional): Previous conversation messages for context.
                                 If None, starts a new conversation.
        
    Returns:
        tuple: (AI response, updated message history including the new exchange)
    """
    try:
        # Initialize conversation with system message if no history provided
        if messages is None:
            conversation_messages = [
                {"role": "system", "content": SYSTEM_MESSAGE}
            ]
        else:
            conversation_messages = messages.copy()
        
        # Add new user message
        conversation_messages.append({"role": "user", "content": user_message})
        
        # Use the chat method with conversation history
        response = co_v2.chat(
            model="command-a-03-2025",
            messages=conversation_messages,  
            temperature=0.1
        )
        
        # Fallback response in case of no content
        assistant_response = "No response received from the AI service."

        # Extract text from response
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            content = response.message.content
            if isinstance(content, list) and len(content) > 0:
                content_obj = content[0]
                if hasattr(content_obj, 'text'):
                    assistant_response = content_obj.text.strip()
        
        # Add assistant response to conversation history
        conversation_messages.append({"role": "assistant", "content": assistant_response})
        return assistant_response, conversation_messages
        
    except Exception as e:
        error_msg = f"Error getting travel guidance: {str(e)}"

# Test function (remove in production)
def test_service():
    """Test the travel advice service with both single and multi-turn conversations"""
    print("=== Testing Single-Turn Conversation ===")
    response1, history1 = get_travel_guidance("What are the top attractions in Paris?")
    print(f"Response: {response1[:200]}...")
    print(f"History length: {len(history1)} messages")
    
    print("\n=== Testing Multi-Turn Conversation ===")
    # Start conversation
    response2, history = get_travel_guidance("What are good places to visit in Japan?")
    print(f"Turn 1: {response2[:150]}...")
    
    # Continue conversation with context
    response3, history = get_travel_guidance("What about the food there?", history)
    print(f"Turn 2: {response3[:150]}...")
    
    # Another follow-up
    response4, history = get_travel_guidance("How much should I budget for a week?", history)
    print(f"Turn 3: {response4[:150]}...")
    
    print(f"\nConversation has {len(history)} messages in total")

if __name__ == "__main__":
    # Only run test when script is executed directly
    test_service()
