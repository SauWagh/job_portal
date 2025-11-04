from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


mob_regex = RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit mobile number")

class JobDetails(models.Model): 
    CATEGORY_CHOICES = [
    ('it', 'IT / Software'),
    ('civil', 'Civil Engineering'),
    ('mechanical', 'Mechanical Engineering'),
    ('electronic', 'Electronics / Electrical'),
    ('chemical', 'Chemical Engineering'),
    ('biotech', 'Biotechnology'),
    ('healthcare', 'Healthcare / Medical'),
    ('finance', 'Finance / Banking'),
    ('marketing', 'Marketing / Sales'),
    ('hr', 'Human Resources'),
    ('education', 'Education / Teaching'),
    ('research', 'Research / Development'),
    ('design', 'Graphic / UX / UI Design'),
    ('legal', 'Legal / Law'),
    ('hospitality', 'Hospitality / Tourism'),
    ('media', 'Media / Journalism'),
    ('telecom', 'Telecommunications'),
    ('consulting', 'Consulting'),
    ('manufacturing', 'Manufacturing'),
    ('logistics', 'Logistics / Supply Chain'),
    ('others', 'Other'),
]


    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('in_office', 'In-Office'),
    ]

    category = models.CharField("Category", max_length=100, choices=CATEGORY_CHOICES, default='it')
    job_type = models.CharField("Job Type", max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    company_name = models.CharField("Company Name", max_length=100)
    job_title = models.CharField("Job Title", max_length=100)
    job_location = models.CharField("Location", max_length=100)
    salary = models.FloatField("Salary Range", blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs_posted',null=True, blank=True)
    def __str__(self):
        return self.company_name


class CandidateDescription(models.Model): 
    job = models.OneToOneField(JobDetails, on_delete=models.CASCADE, related_name='can_des', null=True, blank=True)
    min_experience = models.PositiveIntegerField("Minimum Experience (years)", blank=True, null=True)
    max_experience = models.PositiveIntegerField("Maximum Experience (years)", blank=True, null=True)
    education_required = models.CharField("Required Education", max_length=100, blank=True, null=True)
    skills_required = models.TextField("Required Skills", blank=True, null=True)

    def __str__(self):
        return f"{self.job.company_name} - Candidate Description" if self.job else "Candidate Description"


class JobDescription(models.Model):
    job = models.OneToOneField(JobDetails, on_delete=models.CASCADE, related_name='job_des', null=True, blank=True)
    job_description = models.TextField("Job Description")
    ideal_candidate_profile = models.TextField("Ideal Candidate Profile", blank=True, null=True)
    application_deadline = models.DateField("Application Deadline", null=True, blank=True)

    def __str__(self):
        return f"{self.job.company_name} - Job Description" if self.job else "Job Description"


class Communication(models.Model):
    job = models.OneToOneField(JobDetails, on_delete=models.CASCADE, related_name='comm', null=True, blank=True)
    contact_email = models.EmailField("Contact Email")
    contact_number = models.CharField("Contact Number", max_length=10, unique=True, validators=[mob_regex])

    def __str__(self):
        return f"{self.job.company_name} - Contact Info" if self.job else "Contact Info"


class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]

    email = models.EmailField('Email', unique=True)
    mobile = models.CharField('Mobile number', max_length=10, unique=True, validators=[mob_regex])
    role = models.CharField('Role', max_length=20, choices=ROLE_CHOICE, default='job_seeker')

    def __str__(self):
        return f'{self.username} ({self.role})'
    

class JobApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobDetails, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f'{self.user.username} applied for {self.job.job_title}'