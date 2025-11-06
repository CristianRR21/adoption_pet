from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/iniciarSesion')
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'role') or request.user.role != 'administrator':
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper
