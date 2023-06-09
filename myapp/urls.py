from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'myapp'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Job listings
    path('job_listings/', views.job_listings, name='job_list'),
    path('job_listings/<int:job_id>/', views.job_details, name='job_details'),

    # User registration and login
    path('registration/register/', views.register, name='register'),
    path('registration/login/', auth_views.LoginView.as_view(), name='login'),
    path('registration/logout/', views.logout_view, name='logout'),

    # Employer dashboard
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/job_form/', views.post_job, name='post_job'),
    path('employer/messages/', views.messages, name='messages'),
    path('employer/applications/', views.applications, name='applications'),

    # Apply job
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
]
