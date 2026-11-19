from functools import wraps
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import Admin, Teacher, Student


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if Admin.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Admin privileges required to access this portal.'}, status=403)
    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if Teacher.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Teacher privileges required to access this portal.'}, status=403)
    return _wrapped_view


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if Student.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Student privileges required to access this portal.'}, status=403)
    return _wrapped_view
