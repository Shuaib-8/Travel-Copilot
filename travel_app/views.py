from django.shortcuts import render
from django.http import HttpResponse
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
        
        # If this is an HTMX request, return just the AI response HTML
        if request.headers.get('HX-Request'):
            ai_response_html = f'''
            <div class="flex justify-end">
                <div class="bg-gray-50 rounded-2xl p-4 shadow-sm border border-gray-100" style="max-width: 70%; max-height: 25vh; overflow-y: auto; word-wrap: break-word; margin-right: 0; margin-left: 15%;">
                    <div class="flex items-start space-x-3">
                        <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="text-sm font-medium text-gray-900 mb-2">AI Travel Assistant</div>
                            <div class="text-gray-700 leading-relaxed text-sm" style="word-break: break-word; overflow-wrap: break-word;">{response}</div>
                        </div>
                    </div>
                </div>
            </div>
            '''
            return HttpResponse(ai_response_html)
        
        return render(request, self.template_name, {
            'response': response,
            'messages': updated_messages
        })
