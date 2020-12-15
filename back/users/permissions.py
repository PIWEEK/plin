from rest_framework import permissions


class OnlyAnonCanCreate(permissions.BasePermission):
    """
    Custom permission:
        - only anon user can create
    """

    def has_permission(self, request, view):
        is_anon = not request.user.is_authenticated
        return is_anon



class OnlyMeCanRetrieve(permissions.BasePermission):
    """
    Custom permission:
        - only ME can get my info
    """
    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
