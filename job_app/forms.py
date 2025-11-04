from django.forms import ModelForm
from job_app.models import*
from django import forms


class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetails
        fields = '__all__'

class CandidateDescriptionForm(forms.ModelForm):
    class Meta:
        model = CandidateDescription
        fields = '__all__'

class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = '__all__'
        widgets = {
            'application_deadline' : forms.DateInput(attrs={'type':'Date'})
        }

class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = '__all__'



from django import forms
from .models import CustomUser

class RegisterProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'role', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")



        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



