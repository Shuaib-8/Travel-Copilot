import os
from dotenv import load_dotenv
from cohere import ClientV2
from pathlib import Path

# Load environment variables from .env file (local development only)
# In production/Docker, environment variables should be set directly
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'

# Only load .env file if it exists and we're not in a containerized environment
if env_path.exists() and not os.getenv('DOCKER_CONTAINER'):
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
        
        # Add new user message to conversation history
        conversation_messages.append({"role": "user", "content": user_message})
        
        # Use the chat method with conversation history
        response = co_v2.chat(
            model="command-a-03-2025",
            messages=conversation_messages,  
            temperature=0.1
        )
        
        # Fallback response in case of no content (likely hit domain refusal or rate limit)
        assistant_response = "No response received from the AI service."

        # Extract text from response
        if hasattr(response.message, 'content'):
            content = response.message.content
            if isinstance(content, list) and len(content) > 0:
                content_obj = content[0] # object is a single item in the list
                if hasattr(content_obj, 'text'):
                    assistant_response = content_obj.text.strip()
        
        # Add assistant response to conversation history
        conversation_messages.append({"role": "assistant", "content": assistant_response})
        return assistant_response, conversation_messages
        
    except Exception as e:
        error_msg = f"Error getting travel guidance: {str(e)}"
        # Return error message and empty conversation history
        return error_msg, [{"role": "system", "content": SYSTEM_MESSAGE}]
