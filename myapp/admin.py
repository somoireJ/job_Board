from django.contrib import admin
from .models import JobListing, JobApplication, UserProfile

class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'industry', 'posted_at', 'owner')
    list_filter = ('location', 'industry', 'job_type')
    search_fields = ('title', 'owner__username')

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_listing', 'applicant', 'application_date')
    list_filter = ('job_listing__location', 'job_listing__industry')
    search_fields = ('job_listing__title', 'applicant__username')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'resume')
    search_fields = ('user__username', 'user__email')

admin.site.register(JobListing, JobListingAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
