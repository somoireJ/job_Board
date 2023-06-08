from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'myapp'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Job listings
    path('job_listings/', views.job_listings, name='job_list'),
    path('job_listings/<int:pk>/', views.job_details, name='job_details'),

    # User registration and login
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # Employer dashboard
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('job_form/', views.post_job, name='post_job'),
    path('applications/', views.JobApplication, name='applications'),
    path('messages/', views.messages, name='messages'),

   #apply jobs
    path('apply_job/<int:pk>/', views.apply_job, name='apply_job'),
    # Error pages
    # path('404/', views.error_404, name='error_404'),
    # path('500/', views.error_500, name='error_500'),
]
