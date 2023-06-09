from django.contrib import admin
from .models import JobListing, JobApplication, UserProfile, User, Applicant, Employer


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


class UserAdmin(admin.ModelAdmin):
    pass


class ApplicantAdmin(admin.ModelAdmin):
    pass


class EmployerAdmin(admin.ModelAdmin):
    pass


admin.site.register(JobListing, JobListingAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Employer, EmployerAdmin)
