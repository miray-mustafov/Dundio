from functools import wraps
from django.conf import settings
from django.shortcuts import redirect


def custom_login_required(view):
    @wraps(view)
    def wrap(request, *args, **kwargs):
        if request.custom_user:
            return view(request, *args, **kwargs)
        return redirect(settings.LOGIN_URL)

    return wrap


def custom_login_forbidden(view):
    @wraps(view)
    def wrap(request, *args, **kwargs):
        if not request.custom_user:
            return view(request, *args, **kwargs)
        return redirect(settings.INDEX_URL)

    return wrap
