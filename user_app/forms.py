from django import forms
from user_app.models import UserDetail

class UserForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        exclude = ['user']
        widgets = {
            'resume_upload': forms.ClearableFileInput(attrs={'accept': '.pdf'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'skills': forms.Textarea(attrs={'rows': 3}),
        }
