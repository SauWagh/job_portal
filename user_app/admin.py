from django.contrib import admin
from user_app.models import*
from job_app.models import*

# Register your models here.
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "gender", "experience_years")
    search_fields = ("full_name", "phone_number", "skills")
    list_filter = ("gender", "highest_education")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "user", "applied_for")  # use the correct field name
    list_filter = ("job", "applied_for") 