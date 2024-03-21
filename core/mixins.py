from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from account.models import CustomUser


class RegularUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated or request.user.role != CustomUser.USER:
            raise PermissionDenied('You must be a regular user to access this page.')
        return super().dispatch(request, *args, **kwargs)


class OrganizerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated or request.user.role != CustomUser.ORGANIZER:
            raise PermissionDenied("You must be an organizer to access this page.")
        return super().dispatch(request, *args, **kwargs)

