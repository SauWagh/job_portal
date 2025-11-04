from django.shortcuts import render
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import yaml

# Create your views here.

from django.http import JsonResponse
from django.shortcuts import render
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('SimpleBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

def chat_page(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)
    return render(request, 'chatbot_app/chatbot.html',{'profile': profile})

def get_response(request):
    user_message = request.GET.get("message")
    response = chatbot.get_response(user_message)
    user_message.delete()
    return JsonResponse({"response": str(response)})
