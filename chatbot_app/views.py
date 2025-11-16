import os
from django.shortcuts import render
from django.http import JsonResponse
from chatterbot import ChatBot

# Load ChatterBot using Render's PostgreSQL database
chatbot = ChatBot(
    'SimpleBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=os.environ["DATABASE_URL"]   # ⭐ ADD HERE
)

def chat_page(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user, 'detail', None)
    return render(request, 'chatbot_app/chatbot.html', {'profile': profile})

def get_response(request):
    user_message = request.GET.get("message")
    response = chatbot.get_response(user_message)
    return JsonResponse({"response": str(response)})
