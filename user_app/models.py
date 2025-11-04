from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
import datetime

mob_regex = RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit mobile number")

class UserDetail(models.Model):
    
    GENDER_CHOICE = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="detail")

    full_name = models.CharField("Full Name", max_length=100, blank=True, null=True)
    phone_number = models.CharField("Phone Number", max_length=15, validators=[mob_regex])
    gender = models.CharField("Gender", max_length=20, choices=GENDER_CHOICE, default="Other")
    date_of_birth = models.DateField("Birth Of Date", null=True, blank=True)
    profile_picture = models.ImageField("Profile Picture", upload_to="profile_pics/", null=True, blank=True)

    highest_education = models.CharField("Highest Education", max_length=100, blank=True, null=True)
    skills = models.TextField("Skills", blank=True, null=True)
    experience_years = models.PositiveIntegerField("Experience Years", default=0, blank=True)
    current_position = models.CharField("Current Position", max_length=100, blank=True, null=True)
    preferred_job_location = models.CharField("Preferred Job Location", max_length=100, blank=True, null=True)

    resume_upload = models.FileField("Resume Upload", upload_to="resumes/", blank=True, null=True)
    linkedin_profile = models.URLField("LinkedIn Profile", blank=True, null=True)
    portfolio_link = models.URLField("Portfolio Link", blank=True, null=True)
    project_link = models.URLField("Project Link", blank=True, null=True)

    class Meta:
        verbose_name = "User Detail"
        verbose_name_plural = "User Details"
        ordering = ["full_name"]

    def profile_completed(self):
        fields = {
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'profile_picture': self.profile_picture,
            'highest_education': self.highest_education,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'preferred_job_location': self.preferred_job_location,
            'resume_upload': self.resume_upload,
            'linkedin_profile': self.linkedin_profile,
            'portfolio_link': self.portfolio_link,
            'project_link': self.project_link,
        }

        filled = sum(1 for v in fields.values() if v not in [None, "", 0])
        total = len(fields)

        return int((filled / total) * 100) if total > 0 else 0 

 
    def __str__(self):
        return self.full_name or self.user.username
    
class Application(models.Model):
    job = models.ForeignKey('job_app.JobDetails', on_delete=models.CASCADE, related_name='application')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_application')
    applied_for = models.DateField(auto_now_add=True)

    STATUS_CHOICE = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    profile_status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.job.title} ({self.profile_status})"




class SavedJob(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_jobs'
    )
    job = models.ForeignKey(
        'job_app.JobDetails',
        on_delete=models.CASCADE,
        related_name='saved_by'
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f'{self.user.username} saved {self.job.job_title}'
