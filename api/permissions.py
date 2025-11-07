from rest_framework import permissions

class UserPermissions(permissions.BasePermission):
    """permission of users """

    def has_object_permission(self, request, view, obj):
        """here we're  trying  to know of the user is authenticated  """

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.is_authenticated and obj==request.user)



    def has_permission(self, request, view):

        """here we check if the user is authenticated or anonymous"""


        if view.basename == 'users':

            if request.user.is_anonymous:
                return request.method in permissions.SAFE_METHODS
            return request.user.is_authenticated
        return True