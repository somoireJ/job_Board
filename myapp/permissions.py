# from rest_framework.permissions import BasePermission


# class IsApplicantUser(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_applicant)


# class IsEmployerUser(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_employer)
##
#working more on authentication
from rest_framework.permissions import BasePermission


class IsJobSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_superuser


class IsApplicantOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.applicant or request.user.is_superuser
