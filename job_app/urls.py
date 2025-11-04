from django.urls import path
from job_app.views import*
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', home, name='home'),
    path('register/', user_registration, name='register'),
    path('welcome/', welcome, name='welcome'),
    path('create-it-job/', create_it_job, name='create_it_job'),
    path('add/', add_job, name='add_job'),
    path('list/',Job_list, name='job_list'),
    path('update/<int:id>',update_job, name='update_job'),
    path('delete/<int:id>',job_delete,name='job_delete'),
    path('about/',about, name = 'about'),
    path('contact/',contact,name='contact'),
    path('filter',job_filters, name="filter"),
    path('apply_job/',apply_job,name='apply_job'),
    path('edit_before_applying_job/<int:job_id>/',edit_profie_before_applying,name='edit_before_applying_job'),
    

    path('login/', auth_views.LoginView.as_view(template_name='job_app/login.html'), name='login'),
]
