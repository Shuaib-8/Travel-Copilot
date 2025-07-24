from django.shortcuts import render
from core.llm_service import get_travel_guidance

def travel_guidance_view(request):
    """
    View to handle travel guidance requests.
    """
    response = None
    updated_messages = None
    
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '')
        messages = request.POST.getlist('messages')  # Assuming messages are sent as a list
        response, updated_messages = get_travel_guidance(user_message, messages)
    
    return render(request, 'travel_app/travel_guidance.html', {
        'response': response,
        'messages': updated_messages
    })
