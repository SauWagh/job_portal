from resume_app.models import *
from django import forms
from django.forms import modelformset_factory


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        exclude = ['user']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter your address'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn profile link'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub profile link'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Portfolio Website'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = "__all__"
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Degree'}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University/College'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Year of passing'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grade/CGPA'}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = "__all__"
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role/Position'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration e.g. Jan 2020 - Dec 2022'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Job responsibilities'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = "__all__"
        widgets = {
            'skill': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skill name'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Project Title'}),
            'description' : forms.TextInput(attrs = { 'class' : 'form-control','placeholder' : 'Description'}),
            'technologies' : forms.TextInput(attrs={'class' : 'form-control','placeholder' : 'Technologis Used'}),
            'link' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Project Link / GitHub'}),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control",'placeholder':'Certification Name'}),
            'organization': forms.TextInput(attrs={'class':"form-control",'placeholder':'Issued By"'}),
            'issue_date': forms.TextInput(attrs={'class':"form-control",'placeholder':'Issue Date'}),
            'expiry_date': forms.TextInput(attrs={'class':"form-control",'placeholder':'Expiry Date'}),
            'credential_id': forms.TextInput(attrs={'class':"form-control",'placeholder':'Credential ID'}),
            'credential_url': forms.TextInput(attrs={'class':"form-control",'placeholder':'Credential URL'}),
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = "__all__"
        widgets = {
            'language' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Language'}),
            'proficiency' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Proficiency'}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = "__all__"
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Title'}),
            'description' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Description'}),
            'date' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Date'}),
        }


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = "__all__"
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Publication Title'}),
            'journal' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Journal / Conference'}),
            'date' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Publication Date'}),
            'link' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Link'}),
        }


EducationFormSet = modelformset_factory(Education, form=EducationForm, extra=1, can_delete=True)
ExperienceFormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1, can_delete=True)
SkillFormSet = modelformset_factory(Skill, form=SkillForm, extra=1, can_delete=True)
ProjectFormSet = modelformset_factory(Project, form=ProjectForm, extra=1, can_delete=True)
CertificationFormSet = modelformset_factory(Certification, form=CertificationForm, extra=1, can_delete=True)
LanguageFormSet = modelformset_factory(Language, form=LanguageForm, extra=1, can_delete=True)
AchievementFormSet = modelformset_factory(Achievement, form=AchievementForm, extra=1, can_delete=True)
PublicationFormSet = modelformset_factory(Publication, form=PublicationForm, extra=1, can_delete=True)