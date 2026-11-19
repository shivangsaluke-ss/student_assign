from functools import wraps
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'admin_profile') or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Access Denied: Administrator access required.'}, status=403)
    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'teacher_profile'):
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Access Denied: Teacher access required.'}, status=403)
    return _wrapped_view


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'student_profile'):
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Access Denied: Student access required.'}, status=403)
    return _wrapped_view
