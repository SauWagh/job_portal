from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

# Regex validator for mobile numbers
mob_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="Enter a valid 10-digit mobile number")


class PersonalInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    
    full_name = models.CharField("Full Name", max_length=100)
    email = models.EmailField("Email ID")
    phone = models.CharField("Phone Number", max_length=10, validators=[mob_regex])
    address = models.TextField("Address", blank=True)
    linkedin = models.URLField("LinkedIn Profile", blank=True,null=True)
    github = models.URLField("GitHub Profile", blank=True,null=True)
    portfolio = models.URLField("Portfolio Website", blank=True,null=True)

    def __str__(self):
        return self.full_name

class Education(models.Model):
    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="education", verbose_name="Resume",blank=True, null=True)
    
    degree = models.CharField("Degree", max_length=100,blank=True,null=True)
    university = models.CharField("University", max_length=200,blank=True,null=True)
    year = models.CharField("Year of Passing", max_length=10,blank=True,null=True)
    grade = models.CharField("Grade / CGPA", max_length=20,blank=True,null=True)

    def __str__(self):
        return f"{self.degree} - {self.university}"

class Experience(models.Model):
    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="experience", verbose_name="Resume", blank=True, null=True)
    
    company = models.CharField("Company Name", max_length=200 ,blank=True, null=True)
    role = models.CharField("Role / Position", max_length=100,blank=True, null=True)
    duration = models.CharField("Duration", max_length=50,blank=True, null=True)
    description = models.TextField("Job Description",blank=True, null=True)

    def __str__(self):
        return self.company if self.company else "No Experience"

class Skill(models.Model):
    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="skills", verbose_name="Resume",blank=True, null=True)
    
    skill = models.CharField("Skill", max_length=100,blank=True, null=True)

    def __str__(self):
        return self.skill if self.skill else 'No Skill'

class Project(models.Model):
    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="projects", verbose_name="Resume",blank=True, null=True)
    
    title = models.CharField("Project Title", max_length=200,blank=True,null=True)
    description = models.TextField("Description", blank=True,null=True)
    technologies = models.CharField("Technologies Used", max_length=200, blank=True,null=True)
    link = models.URLField("Project Link / GitHub", blank=True,null=True)

    def __str__(self):
        return self.title

class Certification(models.Model):
    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="certifications", verbose_name="Resume",blank=True, null=True)
    
    name = models.CharField("Certification Name", max_length=200)
    organization = models.CharField("Issued By", max_length=200)
    issue_date = models.DateField("Issue Date", blank=True, null=True)
    expiry_date = models.DateField("Expiry Date", blank=True, null=True)
    credential_id = models.CharField("Credential ID", max_length=100, blank=True)
    credential_url = models.URLField("Credential URL", blank=True)

    def __str__(self):
        return self.name

class Language(models.Model):

    LANGUAGE_CHOICE = [
    ('basic', 'Basic'),
    ('intermediate', 'Intermediate'),
    ('fluent', 'Fluent'),
    ('native', 'Native'),
    ]

    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="languages", verbose_name="Resume",blank=True , null=True)
    
    language = models.CharField("Language", max_length=50)
    proficiency = models.CharField("Proficiency", max_length=20, choices=LANGUAGE_CHOICE,default='basic')

    def __str__(self):
        return f"{self.language} ({self.proficiency})"

class Achievement(models.Model):
    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="achievements", verbose_name="Resume",blank=True,null=True)
    
    title = models.CharField("Title", max_length=200,blank=True,null=True)
    description = models.TextField("Description", blank=True,null=True)
    date = models.DateField("Date", blank=True, null=True)

    def __str__(self):
        return self.title

class Publication(models.Model):
    resume = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name="publications", verbose_name="Resume",blank=True,null=True)
    
    title = models.CharField("Publication Title", max_length=200)
    journal = models.CharField("Journal / Conference", max_length=200, blank=True,null=True)
    date = models.DateField("Publication Date", blank=True, null=True)
    link = models.URLField("Link", blank=True,null=True)

    def __str__(self):
        return self.title
