from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from contact_app.form import*

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"From: {name} <{email}>\n\n{message}"

            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['sw750978@gmail.com'],
                fail_silently=False,
            )

            return redirect('/email_success/')
    else:
        form = ContactForm()

    return render(request, 'contact_app/complaint_email.html', {'form': form})


def email_success(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)
    return render(request, 'contact_app/email_success.html',{'profile' :profile})