from rest_framework import permissions


class IsAuthenticatedInPutReq(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT":
            return request.user and request.user.is_authenticated
        return True
