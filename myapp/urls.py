from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('job_list/', views.job_listings, name='job_list'),
    path('job_details/<int:job_id>/', views.job_details, name='job_details'),
    path('registration/register/', views.register, name='register'),
    path('registration/login/', views.user_login, name='login'),
    path('registration/logout/', views.user_logout, name='logout'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/post_job/', views.post_job, name='post_job'),
    path('employer/applications/', views.applications, name='applications'),
    path('employer/view_application/<int:job_id>/<int:application_id>/', views.view_application, name='view_application'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('messages/<int:application_id>/', views.send_message, name='message'),
    path('application_details/<int:application_id>/', views.application_details, name='application_details'),
]
