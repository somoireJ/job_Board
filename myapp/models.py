# from django.db import models
# from django.db.models.signals import post_save
# from django.conf import settings
# from django.dispatch import receiver
# from django.contrib.auth.models import AbstractUser
# from rest_framework.authtoken.models import Token


# class User(AbstractUser):
#     is_applicant = models.BooleanField(default=False)
#     is_employer = models.BooleanField(default=False)
#     # is_admin = models.BooleanField(default=False)

#     def __str__(self):
#         return self.username


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# class Applicant(models.Model):
#     user = models.OneToOneField(User, related_name="applicant", on_delete=models.CASCADE)
#     phone = models.CharField(max_length=12, null=True, blank=True)
#     skills = models.CharField(max_length=100, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     portfolio = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.user.username


# class Employer(models.Model):
#     user = models.OneToOneField(User, related_name="Employer", on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=200, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return self.user.username





from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_employer = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.user.username

class JobListing(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
        ('Internship', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    posted_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, default='Unknown', blank=True)
    application_instructions = models.TextField(default='Please provide application instructions')

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/', default='default_resume.pdf')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Job Application for {self.job_listing.title} by {self.applicant.username}"
