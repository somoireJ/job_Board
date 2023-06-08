# from django.http import request
# from rest_framework import generics, permissions, status
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from .serializers import ApplicantSignupSerializer, EmployerSignupSerializer, UserSerializer
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.views import APIView
# from .permissions import IsApplicantUser, IsEmployerUser


# class ApplicantSignupView(generics.GenericAPIView):
#     serializer_class = ApplicantSignupSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": token.key,
#             "message": "Account created successfully"
#         })


# class EmployerSignupView(generics.GenericAPIView):
#     serializer_class = EmployerSignupSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": token.key,
#             "message": "Account created successfully"
#         })


# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         is_applicant = user.is_applicant
#         is_employer = user.is_employer
 
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'is_applicant': user.is_applicant,
#             'is_employer': user.is_employer,
            
#         })


# class LogoutView(APIView):
#     def post(self, request, format=None):
#         request.auth.delete()
#         return Response(status=status.HTTP_200_OK)


# class ApplicantOnlyView(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated & IsApplicantUser]
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user


# class EmployerOnlyView(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated & IsEmployerUser]
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user

###

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, logout
from .models import JobListing, JobApplication, UserProfile
from .forms import JobApplicationForm, UserCreationForm


def home(request):
    # Retrieve featured job listings
    featured_listings = JobListing.objects.order_by('-posted_at')[:5]
    
    # Add search functionality here based on location, industry, and job type criteria
    
    context = {
        'featured_listings': featured_listings,
    }
    return render(request, 'home.html', context)

def job_listings(request):
    # Retrieve all job listings or filter based on search criteria
    
    context = {
        'job_listings': job_listings,
    }
    return render(request, 'job_listings/job_list.html', context)

def job_details(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'job_listings/job_details.html', context)

# @login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        
        if form.is_valid():
            application = form.save(commit=False)
            application.job_listing = job
            application.applicant = request.user
            application.save()
            return redirect('job/listings/job_details.html', job_id=job_id)
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'apply_job.html', context)

# @login_required
@login_required
def employer_dashboard(request):
    # Retrieve job listings posted by the logged-in employer
    job_listings = JobListing.objects.filter(owner=request.user)
    
    # Retrieve job applications received for the employer's job listings
    job_applications = JobApplication.objects.filter(job_listing__in=job_listings)
    
    user_accounts = []  # Placeholder for user accounts data retrieval
    analytics = []  # Placeholder for analytics data retrieval
    
    context = {
        'job_listings': job_listings,
        'job_applications': job_applications,
        'user_accounts': user_accounts,
        'analytics': analytics,
    }
    return render(request, 'employer/dashboard.html', context)

##

# @login_required
def admin_dashboard(request):
    # Retrieve user accounts, job listings, and analytics information
    
    context = {
        'user_accounts': user_accounts,
        'job_listings': job_listings,
        'analytics': analytics,
    }
    return render(request, 'admin_dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('myapp:home') 


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('myapp:home')  
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def post_job(request):
    if request.method == 'POST':
        # Process the form submission and save the job listing
        # ...
        return redirect('myapp:employer_dashboard')  # Redirect to the employer dashboard after successful job posting
    else:
        # Display the form to post a job listing
        return render(request, 'employer/job_form.html')


def messages(request):
    # Retrieve and process messages
    # ...

    context = {
        # Provide the necessary data to the template
        # ...
    }
    return render(request, 'employer/messages.html', context)