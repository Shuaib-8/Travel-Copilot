from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from core.llm_service import get_travel_guidance


class TravelGuidanceView(View):
    """
    Class-based view to handle travel guidance requests.
    """
    template_name = 'travel_app/travel_guidance.html'
    
    def get(self, request):
        """Handle GET requests - show the form"""
        # Check if restart parameter is present
        if request.GET.get('restart') == 'true':
            request.session.pop('conversation_history', None)
            
        return render(request, self.template_name, {
            'conversation_history': request.session.get('conversation_history', []),
            'messages': None
        })
    
    def post(self, request):
        """Handle POST requests - process travel guidance"""
        user_message = request.POST.get('user_message', '')
        messages_list = request.POST.getlist('messages')
        # Convert empty list to None for initial conversation turn
        messages = messages_list if messages_list else None
        response, updated_messages = get_travel_guidance(user_message, messages)
        
        # Store conversation in session for persistence
        if 'conversation_history' not in request.session:
            request.session['conversation_history'] = []
        
        request.session['conversation_history'].append({
            'user_message': user_message,
            'ai_response': response
        })
        request.session.modified = True
        
        # Handle HTMX requests with template partial
        if request.headers.get('HX-Request'):
            conversation_html = render_to_string(
                'travel_app/partials/conversation_pair.html',
                {
                    'user_message': user_message,
                    'ai_response': response
                }
            )
            return HttpResponse(conversation_html)
        
        return render(request, self.template_name, {
            'conversation_history': request.session.get('conversation_history', []),
            'messages': updated_messages
        })
