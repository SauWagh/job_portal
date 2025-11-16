from django.urls import path
from chatbot_app.views import*

urlpatterns = [
    path('chat_page/',chatbot_page,name='chat_page'),
    path('chatbot/',simple_chat, name='chatbot'),
]
