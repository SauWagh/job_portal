from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from job_app.forms import*
from job_app.models import*
from django.db.models import Prefetch
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from user_app.models import*
from user_app.forms import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import traceback
import logging
logger = logging.getLogger(__name__)


def home(request):

    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

    query = request.GET.get('q')
    jobs = JobDetails.objects.all().select_related('can_des','job_des','comm')

    if query:
        jobs = jobs.filter(
            Q(job_title__icontains = query) |
            Q(category__icontains = query) | 
            Q(company_name__icontains = query) |
            Q(job_location__icontains = query) |
            Q(job_type__icontains = query) |
            Q(salary__icontains = query) 
        )
        return redirect(f'/list/?q={query}')
    return render(request, 'job_app/home.html',{'jobs' : jobs,'profile' : profile})


def welcome(request):
    return render(request, 'job_app/welcome.html')


def user_registration(request):
    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)

            if user.role == 'employer':
                return redirect('add_job')
            elif user.role == 'job_seeker':
                return redirect('job_list')
        
    else:
        form = RegisterProfileForm()
    return render(request, 'job_app/register.html', {'form':form})


def create_it_job(request):
    form = JobDetailForm()

    if request.method == 'POST':
        form = JobDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/welcome/')  # Or wherever you want to redirect

    context = {'form': form}
    return render(request, 'job_app/create_it_job.html', context)

@login_required
def add_job(request):
    if request.method == 'POST':
        job_form = JobDetailForm(request.POST)
        can_des_form = CandidateDescriptionForm(request.POST)
        job_des_form = JobDescriptionForm(request.POST)
        comm_form = CommunicationForm(request.POST)

        if job_form.is_valid() and can_des_form.is_valid() and job_des_form.is_valid() and comm_form.is_valid():
            job_detail = job_form.save(commit=False)
            job_detail.user = request.user
            job_detail.save()

            can_detail = can_des_form.save(commit=False)
            des_detail = job_des_form.save(commit=False)
            comm_detail = comm_form.save(commit=False)

            can_detail.job = job_detail
            des_detail.job = job_detail
            comm_detail.job = job_detail

            can_detail.save()
            des_detail.save()
            comm_detail.save()

            return redirect('job_list')
    else:
        job_form = JobDetailForm()
        can_des_form = CandidateDescriptionForm()
        job_des_form = JobDescriptionForm()
        comm_form = CommunicationForm()

    context = {
        'job_form': job_form,
        'can_des_form': can_des_form,
        'job_des_form': job_des_form,
        'comm_form': comm_form
    }
    return render(request, 'job_app/add_job.html', context)


# def Job_list(request):
#     form = JobDetails.objects.all()
#     can_des = CandidateDescription.objects.all()
#     job_des = JobDescription.objects.all()
#     comm = Communication.objects.all()

#     context = {
#         'form': form,
#         'can_des': can_des,
#         'job_des': job_des,
#         'comm': comm
#     }

#     return render(request, 'job_app/list_of_it_jobs.html', context)





def Job_list(request):
    try:
        profile = None

        if request.user.is_authenticated:
            profile = getattr(request.user, 'detail', None)

        query = request.GET.get('q')
        jobs = JobDetails.objects.all().select_related('can_des', 'job_des', 'comm')

        if query:
            jobs = jobs.filter(
                Q(job_title__icontains=query) |
                Q(category__icontains=query) |
                Q(company_name__icontains=query) |
                Q(job_location__icontains=query) |
                Q(job_type__icontains=query) |
                Q(salary__icontains=query)
            )

        return render(request, 'job_app/list_of_it_jobs.html', {
            'jobs': jobs,
            'profile': profile
        })

    except Exception as e:
        print("ERROR IN Job_list VIEW:", e)
        raise



def edit_profie_before_applying(request,job_id):
    job = get_object_or_404(JobDetails,id = job_id)
    profile ,created = UserDetail.objects.get_or_create(user = request.user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance= profile)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = UserForm(instance=profile)
    return render(request,'job_app/edit_before_applying.html',{'form':form,'job':job})

def apply_job(request,job_id):
    job = get_object_or_404(JobDetails,id = job_id)
    JobApplication = object.get_or_create(user = request.user,job = job)
    return redirect('list')


def job_delete(request,id):
    job_detail = get_object_or_404(JobDetails,pk = id)

    if request.method == 'POST':
        job_detail.delete()
        return redirect('job_list',)
    
    return render (request, 'job_app/delete.html',{'obj':job_delete})

def job_detail(request, id):
    job_detail = get_object_or_404(JobDetails,pk = id)
    can_desc = job_detail.candidatedescription
    job_desc = job_detail.jobdescription
    comm = job_detail.communication
    
    return render (request, 'job_app/detail.html',{
        'job_detail':job_detail,
        'can_desc' : can_desc,
        'job_desc' : job_desc,
        'comm' : comm
    })


def update_job(request,id):
    job_detail = get_object_or_404(JobDetails, pk = id)
    can_desc = job_detail.candidate_description
    job_desc = job_detail.job_description
    comm = job_detail.communication
    
    if request.method == 'POST':
        job_form = JobDetailForm(request.POST,instance = job_detail)
        can_form = CandidateDescriptionForm(request.POST, instance=can_desc)
        job_desc_form = JobDescriptionForm(request.POST, instance=job_desc)
        comm_form = CommunicationForm(request.POST, instance=comm)
        
        if job_form.is_valid() and can_form.is_valid() and job_desc_form.is_valid() and comm_form.is_valid():
            job_form.save()
            can_form.save()
            job_desc_form.save()
            comm_form.save()

            return redirect('job_list')
        
    else:
        job_form = JobDetailForm(instance=job_detail)
        can_form = CandidateDescriptionForm(instance=can_desc)
        job_desc_form = JobDescriptionForm(instance=job_desc)
        comm_form = CommunicationForm(instance= comm)

    return render(request, 'job_app/update.html',{
        'job_form' : job_form,
        'can_form' : can_form,
        'job_desc_form' : job_desc_form,
        'comm_form'  : comm_form
    })


def about(request):
     profile = None
     if request.user.is_authenticated:
        profile = getattr(request.user,'detail',None)

     return render(request, ('job_app/about.html'),{'profile':profile})

def contact(request):
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user,'detail', None)
        
    return render(request,'job_app/contact.html',{'profile' : profile})


def job_filters(request):
    selected_branches = request.GET.getlist('branch')
    
    branch_skills = {
        'IT / Software': ['Python', 'Django', 'JavaScript', 'Java', 'HTML/CSS', 'AI/ML'],
        'Electronics / Electrical': ['Circuit Design', 'IoT'],
        'Civil': ['AutoCAD', 'Project Management'],
        'Mechanical': ['CAD', 'Thermodynamics'],
        'Finance / Banking': ['Accounting', 'Excel', 'Financial Analysis'],
        'Graphic / UX / UI Design': ['Figma', 'Adobe XD', 'Photoshop'],
        'Biotechnology': ['Molecular Biology', 'Genetic Engineering'],
        'Manufacturing': ['Lean Manufacturing', 'Quality Control'],
        'Education / Teaching': ['Curriculum Design', 'Classroom Management'],
        'Other': ['Communication', 'Problem Solving'],
    }

    related_skills = []
    for branch in selected_branches:
        related_skills += branch_skills.get(branch, [])

    context = {
        'selected_branches': selected_branches,
        'related_skills': related_skills
    }
    return render(request, 'jobs.html', context)



