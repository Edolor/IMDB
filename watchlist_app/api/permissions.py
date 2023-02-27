from math import perm
from django.http import HttpResponseNotAllowed
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    "Check if user is an admin then grant access"
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permission for read only request
            return True
        else:
            # Method is unsafe so check if it is
            admin_permission = bool(request.user and request.user.is_staff)
            return admin_permission


class IsReviewUserOrReadOnly(permissions.BasePermission):
    "Check if user is the real user, else read only"
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permission for read only request
            return True
        else:
            # Method is unsafe so check if it is
            return (obj.review_user == request.user) or request.user.is_staff