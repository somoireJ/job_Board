from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import JobListingForm, UserRegistrationForm, UserProfileForm, LoginForm, MessageForm, AdminUserForm, AdminJobListingForm, JobApplicationForm
from .models import JobListing, UserProfile, JobApplication, Message


def home(request):
    return render(request, 'home.html')


@login_required
def job_listings(request):
    job_list = JobListing.objects.all()
    return render(request, 'job_listings/job_list.html', {'job_list': job_list})


@login_required
def job_details(request, job_id):
    job = JobListing.objects.get(pk=job_id)
    return render(request, 'job_listings/job_details.html', {'job': job})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration successful for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def employer_dashboard(request):
    job_list = JobListing.objects.filter(owner=request.user)
    return render(request, 'employer/dashboard.html', {'job_list': job_list})


@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('employer_dashboard')
    else:
        form = JobListingForm()
    return render(request, 'employer/job_form.html', {'form': form})


@login_required
def messages(request):
    user_messages = Message.objects.filter(user=request.user)
    return render(request, 'employer/messages.html', {'messages': user_messages})


@login_required
def apply_job(request, job_id):
    job = JobListing.objects.get(pk=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            messages.success(request, 'Job application submitted successfully.')
            return redirect('job_listings/job_details', job_id=job_id)
    else:
        form = JobApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})



@login_required
def applications(request):
    job_applications = JobApplication.objects.filter(job_listing__owner=request.user)

    context = {
        'job_applications': job_applications,
    }
    return render(request, 'employer/applications.html', context)

