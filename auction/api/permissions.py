from rest_framework.permissions import IsAuthenticated


class HasUserAccount(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and hasattr(request.user, 'useraccount')
