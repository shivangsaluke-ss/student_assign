from functools import wraps
<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
=======
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from .models import Admin, Teacher, Student
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
<<<<<<< HEAD
        if hasattr(request.user, 'admin_profile') or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Access Denied: Administrator access required.'}, status=403)
=======
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if Admin.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Admin privileges required to access this portal.'}, status=403)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
<<<<<<< HEAD
        if hasattr(request.user, 'teacher_profile'):
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Access Denied: Teacher access required.'}, status=403)
=======
        if Teacher.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Teacher privileges required to access this portal.'}, status=403)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    return _wrapped_view


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
<<<<<<< HEAD
        if hasattr(request.user, 'student_profile'):
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Access Denied: Student access required.'}, status=403)
=======
        if Student.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', {'message': 'Student privileges required to access this portal.'}, status=403)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    return _wrapped_view
