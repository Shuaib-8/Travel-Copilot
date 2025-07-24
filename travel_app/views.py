from django.shortcuts import render
from core.llm_service import get_travel_guidance
from django.views import View

class TravelGuidanceView(View):
    """
    Class-based view to handle travel guidance requests.
    """
    template_name = 'travel_app/travel_guidance.html'
    
    def get(self, request):
        """Handle GET requests - show the form"""
        return render(request, self.template_name, {
            'response': None,
            'messages': None
        })
    
    def post(self, request):
        """Handle POST requests - process travel guidance"""
        user_message = request.POST.get('user_message', '')
        messages_list = request.POST.getlist('messages')
        # Convert empty list to None for initial conversation turn
        messages = messages_list if messages_list else None
        response, updated_messages = get_travel_guidance(user_message, messages)
        
        return render(request, self.template_name, {
            'response': response,
            'messages': updated_messages
        })
