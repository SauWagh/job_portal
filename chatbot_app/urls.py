from django.urls import path
from chatbot_app.views import*

urlpatterns = [
    path('chatbot/',chat_page, name='chat_page'),
    path('get-response/', get_response, name='get_response'),
]
