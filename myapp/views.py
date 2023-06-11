from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from myapp.decorators import employer_required, applicant_required, login_required 
from django.contrib import messages, auth
from .forms import JobApplicationForm, UserRegistrationForm, UserLoginForm, JobListingForm, MessageForm
from .models import JobListing, JobApplication, Message, User, Employer, Applicant
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from rest_framework.views import APIView, status, Response
from rest_framework.response import Response

# Home page
def home(request):
    return render(request, 'home.html')

# Job listings
def job_listings(request):
    jobs = JobListing.objects.all()
    return render(request, 'job_listings/job_list.html', {'jobs': jobs})

# Job details
def job_details(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    return render(request, 'job_listings/job_details.html', {'job': job})

# User registration

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your account has been created successfully.')
#             return redirect('myapp:login')
#         else:
#             error_message = "Registration failed. Please correct the errors below."
#             messages.error(request, error_message)
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})


# User registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('myapp:login')
    else:
        form = UserRegistrationForm()

    # Add the invalid form to the context to display the errors
    context = {'form': form}
    return render(request, 'registration/register.html', context)


# User login
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print('User:', user)
            if user is not None:
                login(request, user)
                print('User logged in:', user)
                return redirect(reverse('myapp:home'))
            else:
                messages.error(request, 'Invalid username or password.')
                print('User not logged in:', user)
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


# User logout
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('myapp:home')

# Employer dashboard
@login_required
def employer_dashboard(request):
    job_listings = JobListing.objects.filter(owner=request.user)
    return render(request, 'employer/dashboard.html', {'job_listings': job_listings})

# Post a job
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.owner = request.user
            job_listing.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('myapp:dashboard')
    else:
        form = JobListingForm()
    return render(request, 'employer/job_form.html', {'form': form})

# View received applications
@login_required
def applications(request):
    job_listings = JobListing.objects.filter(owner=request.user)
    return render(request, 'employer/applications.html', {'job_listings': job_listings})

# View application details
@login_required
def view_application(request, job_id, application_id):
    job_listing = get_object_or_404(JobListing, id=job_id, owner=request.user)
    application = get_object_or_404(JobApplication, id=application_id, job_listing=job_listing)
    return render(request, 'employer/applications.html', {'application': application})

# Apply for a job
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_listing = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully.')
            return redirect('myapp:job_details', job_id=job_id)
    else:
        form = JobApplicationForm()
    return render(request, 'employer/application.html', {'form': form, 'job': job})

# Send message
@login_required
def send_message(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, applicant=request.user)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            message = Message(application=application, sender=request.user, text=message_text)
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('myapp:application_details', application_id=application_id)

    return render(request, 'employer/messages.html', {'application': application})

# View application details (applicant)
@login_required
def application_details(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id, applicant=request.user)
    messages = Message.objects.filter(application=application)
    return render(request, 'application.html', {'application': application, 'messages': messages})
