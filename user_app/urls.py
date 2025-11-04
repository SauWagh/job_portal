from django.urls import path
from user_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('user/',user,name='user'),
    path('dashboard/',user_dashboard, name='dashboard'),
    path('job_info/<int:job_id>',job_info, name='job_info'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('edit_before_applying/<int:job_id>', edit_profile_before_applying, name='edit_before_applying'),
    path('emp_pj/',empPostJob,name='emp_pj'),
    path('appllyed_job/',applied_job_list, name='applyed_job_list'),
    path('posted_job/',posted_jon_list,name='posted_jon_list'),
    path('help/',help, name='help'),
    path('rec_help/',recruiter_help,name='recruiter_help'),
    path('settings/',view_settings,name='settings'),
    path('posted_job_detail/<int:job_id>',posted_job_detail,name='posted_job_detail'),
    path('edit_job/<int:job_id>/',posted_job_edit,name='edit_job'),
    path('applicants_detail/<int:applicants_id>',applicants_detail,name='applicants_detail'),
    path('update_applicant_status/<int:applicant_id>',update_applicant_status,name='update_applicant_status'),
    path('update_application/<int:application_id>/<str:new_status>/', update_status, name='update_application'),

    # path('jobs/',job_list, name='job_list'),        x``
    # path('job/<int:job_id>/',job_detail, name='job_detail'), 

    path('job/<int:job_id>/save/', save_job, name='save_job'),
    path('job/<int:job_id>/remove/', remove_job, name='remove_job'),

    path('saved-jobs/',saved_job_list, name='saved_job_list'),
    # path('delete_acc/<int:id>',delete_acc, name='delete_acc')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
