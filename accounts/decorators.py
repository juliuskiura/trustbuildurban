from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You\'re already logged in')
            return redirect('dashboard:dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            
            if request.user.groups.exists():
                # group = request.user.groups.all()[0].name 
                pass
                # if group in allowed_roles:
            return view_func(request, *args, **kwargs)
                # else:
                #     messages.error(request, 'Action not authorized')
                #     return redirect('dashboard')
        return wrapper_func
    return decorator