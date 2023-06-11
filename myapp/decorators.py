from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def is_employer(user):
    return user.is_authenticated and user.profile.is_employer

def is_applicant(user):
    return user.is_authenticated and user.profile.is_applicant

def employer_required(view_func):
    decorated_view_func = user_passes_test(
        is_employer,
        login_url='myapp:login',
        redirect_field_name=None
    )(view_func)
    return decorated_view_func

def applicant_required(view_func):
    decorated_view_func = user_passes_test(
        is_applicant,
        login_url='myapp:login',
        redirect_field_name=None
    )(view_func)
    return decorated_view_func

def login_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated,
        login_url='myapp:login',
        redirect_field_name=None
    )(view_func)
    return decorated_view_func
