from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps
from account.models import CustomUser


def user_is_regular(function):
    @login_required
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.role != CustomUser.USER:
            raise PermissionDenied("Only regular users can access this view")
        return function(request, *args, **kwargs)
    return wrap


def user_is_organizer(function):
    @login_required
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.role != CustomUser.ORGANIZER:
            raise  PermissionDenied("Only organizers can access this view")
        return function(request, *args, **kwargs)
    return wrap