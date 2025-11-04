from django.urls import path
from resume_app.views import*

urlpatterns = [
    path('resume/',resume_maker, name='resume'),
    path('resume/<int:resume_id>/preview/<int:template_no>',resume_preview, name='resume_preview'),
    path('resume/<int:resume_id>/choice/',res_choice, name='res_choice'),
]