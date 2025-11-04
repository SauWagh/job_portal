from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from resume_app.forms import *
from resume_app.models import *

def resume_maker(request, resume_id=None):
    profile = getattr(request.user, 'detail', None) if request.user.is_authenticated else None

    if request.method == 'POST':
        per_form = PersonalInfoForm(request.POST)
        edu_formset = EducationFormSet(request.POST, queryset=Education.objects.none(), prefix='education')
        exp_formset = ExperienceFormSet(request.POST, queryset=Experience.objects.none(), prefix='experience')
        skill_formset = SkillFormSet(request.POST, queryset=Skill.objects.none(), prefix='skill')
        ach_formset = AchievementFormSet(request.POST, queryset=Achievement.objects.none(), prefix='achievement')

        print("POST received!")
        print("PersonalInfo valid:", per_form.is_valid())
        print("Education valid:", edu_formset.is_valid())
        print("Experience valid:", exp_formset.is_valid())
        print("Skill valid:", skill_formset.is_valid())
        print("Achievement valid:", ach_formset.is_valid())

        if not per_form.is_valid():
            print("PersonalInfo errors:", per_form.errors)
        if not edu_formset.is_valid():
            print("Education errors:", edu_formset.errors)
        if not exp_formset.is_valid():
            print("Experience errors:", exp_formset.errors)
        if not skill_formset.is_valid():
            print("Skill errors:", skill_formset.errors)
        if not ach_formset.is_valid():
            print("Achievement errors:", ach_formset.errors)

        if per_form.is_valid() and edu_formset.is_valid() and exp_formset.is_valid() and skill_formset.is_valid() and ach_formset.is_valid():
            per_detail = per_form.save(commit=False)
            per_detail.user = request.user
            per_detail.save()

            for form in edu_formset.save(commit=False):
                form.resume = per_detail
                form.save()

            for form in exp_formset.save(commit=False):
                form.resume = per_detail
                form.save()

            for form in skill_formset.save(commit=False):
                form.resume = per_detail
                form.save()

            for form in ach_formset.save(commit=False):
                form.resume = per_detail
                form.save()

            return redirect('res_choice', resume_id=per_detail.id)

    else:
        per_form = PersonalInfoForm()
        edu_formset = EducationFormSet(queryset=Education.objects.none(),prefix='education')
        exp_formset = ExperienceFormSet(queryset=Experience.objects.none(),prefix='experience')
        skill_formset = SkillFormSet(queryset=Skill.objects.none(),prefix='skill')
        ach_formset = AchievementFormSet(queryset=Achievement.objects.none(),prefix='achievement')

    return render(request, 'resume_app/resume.html', {
        'per_form': per_form,
        'edu_formset': edu_formset,
        'exp_formset': exp_formset,
        'skill_formset': skill_formset,
        'ach_formset': ach_formset,
        'profile': profile,
    })



def resume_preview(request, resume_id, template_no=1):
    resume = get_object_or_404(PersonalInfo, id=resume_id)

    context = {
        'resume': resume,
        'education': resume.education.all(),
        'experience': resume.experience.all(),
        'skills': resume.skills.all(),
        'projects': resume.projects.all(),
        'certifications': resume.certifications.all(),
        'languages': resume.languages.all(),
        'achievements': resume.achievements.all(),
        'publications': resume.publications.all(),
    }

    templates = {
        1: "resume_app/resume_preview.html",
        2: "resume_app/resume_preview2.html",
        3: "resume_app/resume_preview3.html",
    }
    template_name = templates.get(template_no, "resume_app/resume_preview.html")

    return render(request, template_name, context)



def res_choice(request,resume_id):
     resume = get_object_or_404(PersonalInfo, id = resume_id)
     return render(request,'resume_app/resume_choice.html',{'resume':resume})

