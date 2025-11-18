from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import UserDetail
from .forms import UserForm
from job_app.models import*
from job_app.forms import*
from user_app.models import*
from django.http import JsonResponse
from django.contrib import messages

# @login_required
# def user(request):
#     try:
#         profile = request.user.detail   # get existing profile
#     except UserDetail.DoesNotExist:
#         profile = None                  # no profile yet → create new

#     if request.method == 'POST':
#         form = UserForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             user_detail = form.save(commit=False)
#             user_detail.user = request.user   # connect to logged-in user
#             user_detail.save()
#             return redirect('user_profile')   # after save go to profile
#     else:
#         form = UserForm(instance=profile)

#     return render(request, 'user_app/edit_profile.html', {'form': form})


# @login_required
# def profile_view(request):
#     user_detail, created = UserDetail.objects.get_or_create(user=request.user)
#     if created:
#         return redirect('edit_profile')
#     else:
#         return render(request, 'user_app/user_profile.html', {'user_form': user_detail})

# @login_required
# def profile_view(request):
#     try:
#         profile = request.user.detail   # OneToOne relation
#     except UserDetail.DoesNotExist:
#         return redirect('edit_profile')  # if no details, go fill them
    
#     return render(request, 'user_app/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    try:
        profile = request.user.detail
    except UserDetail.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_detail = form.save(commit=False)
            user_detail.user = request.user

            # 🔥 IMPORTANT: Save image if uploaded
            if "profile_picture" in request.FILES:
                user_detail.profile_picture = request.FILES["profile_picture"]

            user_detail.save()
            return redirect("user_profile")

    else:
        form = UserForm(instance=profile)

    return render(request, "user_app/edit_profile.html", {
        "form": form
    })



# def user_profile(request, id):

#     profile = get_object_or_404(UserDetail,pk = id)

#     return render(request, 'user_app/user_profile.html',{'profile':profile})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserDetail

@login_required
def user_profile(request):
    profile, created = UserDetail.objects.get_or_create(user=request.user)

    if created:
        return redirect('edit_profile')

    return render(request, 'user_app/user_profile.html', {
        'profile': profile
    })




def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Try to get user detail safely
    try:
        profile = request.user.detail
    except UserDetail.DoesNotExist:
        profile = None

    # Fetch jobs and related objects
    jobs = JobDetails.objects.all().select_related('can_des', 'job_des', 'comm')

    # Handle saved jobs safely
    saved_job_ids = []
    if hasattr(request.user, 'saved_jobs'):
        saved_job_ids = request.user.saved_jobs.values_list('job_id', flat=True)

    # Fetch applied jobs
    applied_job = JobApplication.objects.filter(user=request.user).select_related('job')
    applied_count = applied_job.count()

    # Handle completion safely
    completion = 0
    if profile and hasattr(profile, 'profile_completed'):
        completion = profile.profile_completed()

    completion_class = f"w-{round(completion / 5) * 5}"

    return render(request, 'user_app/dashbord.html', {
        'jobs': jobs,
        'applied_job': applied_job,
        'applied_count': applied_count,
        'profile': profile,
        'completion': completion,
        'completion_class': completion_class,
        'saved_job_ids': saved_job_ids,
    })

def job_info(request,job_id):

    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

    job = get_object_or_404(JobDetails,pk=job_id)
    job_can = CandidateDescription.objects.get(job=job)
    job_des = JobDescription.objects.get(job=job)
    comm = Communication.objects.get(job=job)

    saved_job_ids = request.user.saved_jobs.values_list('job_id', flat=True)
    return render(request, 'user_app/job_info.html', 
        {
        'job': job,
        'job_can' : job_can,
        'job_des' : job_des,
        'comm': comm,
        'saved_job_ids' : saved_job_ids
        })

@login_required
def edit_profile_before_applying(request, job_id):
    job = get_object_or_404(JobDetails, id=job_id)
    profile, created = UserDetail.objects.get_or_create(user=request.user)
 
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserForm(instance=profile)

    return render(request, 'user_app/edit_before_applying.html', {'form': form, 'job': job})

def apply_job(request, job_id):
    job = get_object_or_404(JobDetails, id=job_id)

    application, created = Application.objects.get_or_create(user=request.user, job=job)

    if created:
        messages.success(request, "✅ You have successfully applied for this job!")
    else:
        messages.info(request, "⚠️ You already applied for this job.")

    return redirect('dashboard')

def empPostJob(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

    return render(request,'user_app/emp_pj.html',{'profile' : profile})

def applied_job_list(request):

    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

    jobs = JobDetails.objects.all().select_related('can_des', 'job_des', 'comm')

    applied_job = JobApplication.objects.filter(user=request.user).select_related('job')
    applied_count = applied_job.count()

    print("Applied Jobs:", applied_job)

    try:
        profile = request.user.detail
    except UserDetail.DoesNotExist:
        profile= None

    return render(request, 'user_app/applied_job_list.html', 
                  {'jobs': jobs,
                   'applied_job' : applied_job,
                   'applied_count' : applied_count,
                   'profile' : profile,
                })


@login_required
def posted_jon_list(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)


    jobs_posted = request.user.jobs_posted.all()
    job_count = jobs_posted.count()

    return render(request, 'user_app/posted_jon_list.html', {
        'jobs_posted': jobs_posted,
        'job_count': job_count,
        'profile': profile
    })


def help(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

    return render(request,'user_app/help_user.html',{'profile' : profile})

def recruiter_help(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,"detail",None)

    return render (request,'user_app/recruter_help.html',{'profile':profile})

def view_settings(request):

    profile, created = UserDetail.objects.get_or_create(user=request.user)
    if created:
        return redirect('edit_profile')
    return render(request,'user_app/settings.html',{'profile':profile})


# @login_required
# def delete_acc(request):
#     account = request.user  # only the logged-in user

#     if request.method == "POST":
#         account.delete()
#         return redirect("home")

#     return render(request, "user_app/settings.html", {"account": account})

def posted_job_detail(request,job_id):

    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

    job = get_object_or_404(JobDetails,pk = job_id)
    job_can = getattr(job,'can_des',None)
    job_des = getattr(job,'job_des',None)
    job_com = getattr(job,'comm',None)

    applicants = job.application.all()
    applicants_count = applicants.count()

    return render(request,'user_app/posted_job_detail.html',{
        'job' : job,
        'job_can' : job_can,
        'job_des' : job_des,
        'job_com' : job_com,
        'profile' : profile,
        'applicants'  :applicants,
        'applicants_count' : applicants_count
    })


@login_required
def posted_job_edit(request, job_id):
    job = get_object_or_404(JobDetails, id=job_id, user=request.user)

    job_can = getattr(job, 'can_des', None)
    job_des = getattr(job, 'job_des', None)
    job_com = getattr(job, 'comm', None)

    if request.method == 'POST':
        job_form = JobDetailForm(request.POST, instance=job)
        can_form = CandidateDescriptionForm(request.POST, instance=job_can)
        des_form = JobDescriptionForm(request.POST, instance=job_des)
        comm_form = CommunicationForm(request.POST, instance=job_com)

        if job_form.is_valid() and can_form.is_valid() and des_form.is_valid() and comm_form.is_valid():
            job_form.save()

            can_obj = can_form.save(commit=False)
            can_obj.job = job
            can_obj.save()

            des_obj = des_form.save(commit=False)
            des_obj.job = job
            des_obj.save()

            comm_obj = comm_form.save(commit=False)
            comm_obj.job = job
            comm_obj.save()

            return redirect('posted_job_detail', job_id=job.id)

    else:
        job_form = JobDetailForm(instance=job)
        can_form = CandidateDescriptionForm(instance=job_can)
        des_form = JobDescriptionForm(instance=job_des)
        comm_form = CommunicationForm(instance=job_com)

    context = {
        'job_form': job_form,
        'can_form': can_form,
        'des_form': des_form,
        'comm_form': comm_form,
        'job': job
    }

    return render(request, 'user_app/job_edit.html', context)


def  job_applicants_list(request,job_id):
    job = get_object_or_404(JobDetails,id = job_id,user= request.user)
    applicants = job.application.select_related('user').all()

    return render(request,'user_app/posted_job_detail.html',{
        'job':job,
        'applicants':applicants
        })

def applicants_detail(request,applicants_id):
    application = get_object_or_404(Application, id=applicants_id)

    
    applicant_profile = get_object_or_404(UserDetail,user=application.user)
    profile = getattr(request.user, 'detail', None) 

    return render(request, 'user_app/applicants_detail.html', {
        'applicant_profile': applicant_profile,
        'application' : application,
        'profile' : profile,
    })  

def save_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobDetails, id=job_id)
        SavedJob.objects.get_or_create(user=request.user, job=job)
        return JsonResponse({'saved': True})
    return JsonResponse({'error': 'POST request required'}, status=400)

def remove_job(request, job_id):
    if request.method == 'POST': 
        job = get_object_or_404(JobDetails, id=job_id)
        SavedJob.objects.filter(user=request.user, job=job).delete()
        return JsonResponse({'saved': False})
    return JsonResponse({'error': 'POST request required'}, status=400)



def saved_job_list(request):
    saved_jobs = request.user.saved_jobs.select_related('job').all()  # Fetch all saved jobs
    return render(request, 'user_app/saved_job_list.html', {'saved_jobs': saved_jobs})

def update_applicant_status(request, applicant_id):
    applicant = get_object_or_404(Application, id=applicant_id)

    if request.user != applicant.job.user:
        return HttpResponseForbidden("You cannot change this applicant's status")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICE):
            applicant.profile_status = new_status
            applicant.save()
            messages.success(request, f"{applicant.user.username}'s status updated to {new_status}")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('posted_job_detail', job_id=applicant.job.id)


def update_status(request, application_id, new_status):
    application = get_object_or_404(Application, id=application_id)

    if new_status in ['Accepted', 'Rejected']:
        application.profile_status = new_status
        application.save()
        messages.success(request, f"Application status updated to {new_status}")

    # redirect back to the job detail page (ensure this URL name exists)
    return redirect('posted_job_detail', job_id=application.job.id)
