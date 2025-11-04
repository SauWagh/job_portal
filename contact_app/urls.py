from django.urls import path
from contact_app.views import*

urlpatterns =[
    path('complaint_email/',contact_view,name='complaint_email'),
    path('email_success/',email_success,name='email_success'),
]