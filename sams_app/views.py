import os
<<<<<<< HEAD
=======
import json
from datetime import datetime, timedelta
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
<<<<<<< HEAD
from django.db.models import Count, Avg, Q
from django.conf import settings
from django.http import HttpResponse, Http404

from .models import Admin, Teacher, Student, Course, Enrollment, Assignment, Submission, Evaluation
from .forms import (
    LoginForm, StudentRegistrationForm, CourseForm, TeacherForm,
    StudentAdminForm, AssignmentForm, SubmissionUploadForm, EvaluationForm
=======
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, FileResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q

from .models import Admin, Teacher, Student, Course, Enrollment, Assignment, Submission, Evaluation
from .forms import (
    StudentRegisterForm, LoginForm, CourseForm, TeacherForm, StudentAdminForm,
    EnrollmentForm, AssignmentForm, SubmissionUploadForm, EvaluationForm, AnnouncementForm
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
)
from .decorators import admin_required, teacher_required, student_required


<<<<<<< HEAD
# ========================================================
# PUBLIC VIEWS
# ========================================================

def home(request):
    """Landing page with video hero and role overview."""
    courses_count = Course.objects.count()
    teachers_count = Teacher.objects.count()
    students_count = Student.objects.count()
    submissions_count = Submission.objects.count()
    
    context = {
        'courses_count': courses_count,
        'teachers_count': teachers_count,
        'students_count': students_count,
        'submissions_count': submissions_count,
    }
    return render(request, 'public/home.html', context)


def about(request):
    """Objectives and comparison between existing and proposed system."""
    return render(request, 'public/about.html')


def modules(request):
    """Deep dive into Admin, Teacher and Student modules."""
=======
# ==========================================
# PUBLIC PAGES
# ==========================================

def home(request):
    courses_count = Course.objects.count()
    students_count = Student.objects.count()
    teachers_count = Teacher.objects.count()
    assignments_count = Assignment.objects.count()
    submissions_count = Submission.objects.count()
    
    return render(request, 'public/index.html', {
        'courses_count': courses_count,
        'students_count': students_count,
        'teachers_count': teachers_count,
        'assignments_count': assignments_count,
        'submissions_count': submissions_count,
    })


def about(request):
    return render(request, 'public/about.html')


def modules_page(request):
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    return render(request, 'public/modules.html')


def diagrams(request):
<<<<<<< HEAD
    """Diagrams page: system flow, use-case, class, sequence, ER diagrams."""
    return render(request, 'public/diagrams.html')


def database(request):
    """Database schema documentation for all 8 tables."""
    return render(request, 'public/database.html')


def team(request):
    """Project team and mentor credits."""
    return render(request, 'public/team.html')


def user_login(request):
    """Unified login for Admin, Teacher and Student."""
    if request.user.is_authenticated:
        if hasattr(request.user, 'admin_profile') or request.user.is_superuser:
            return redirect('admin_dashboard')
        elif hasattr(request.user, 'teacher_profile'):
            return redirect('teacher_dashboard')
        elif hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            role = form.cleaned_data.get('role', '')

            # Resolve email to username if user entered email
            user_obj = None
            if '@' in username:
                user_obj = User.objects.filter(email__iexact=username).first()
                if user_obj:
                    username = user_obj.username

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                if hasattr(user, 'admin_profile') or user.is_superuser:
                    return redirect('admin_dashboard')
                elif hasattr(user, 'teacher_profile'):
                    return redirect('teacher_dashboard')
                elif hasattr(user, 'student_profile'):
                    return redirect('student_dashboard')
                return redirect('home')
            else:
                messages.error(request, "Invalid username/email or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'public/login.html', {'form': form})


def user_logout(request):
    """Safely log out user and redirect to home."""
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


def user_register(request):
    """Student registration flow with confirmation."""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
=======
    return render(request, 'public/diagrams.html')


def database_schema(request):
    tables = [
        {
            'name': 'admin',
            'desc': 'Stores administrator credentials, contact information and profile link.',
            'fields': [
                {'name': 'admin_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'admin_name', 'type': 'VARCHAR(50)', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'admin_email', 'type': 'VARCHAR(50)', 'key': 'UNI', 'extra': 'NOT NULL, UNIQUE'},
                {'name': 'admin_password', 'type': 'VARCHAR(100)', 'key': '', 'extra': 'NOT NULL (Hashed)'},
                {'name': 'admin_mobile', 'type': 'VARCHAR(15)', 'key': 'UNI', 'extra': 'NOT NULL, UNIQUE'},
            ]
        },
        {
            'name': 'teacher',
            'desc': 'Faculty records including academic department and login association.',
            'fields': [
                {'name': 'teacher_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'teacher_name', 'type': 'VARCHAR(50)', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'teacher_email', 'type': 'VARCHAR(50)', 'key': 'UNI', 'extra': 'NOT NULL, UNIQUE'},
                {'name': 'department', 'type': 'VARCHAR(50)', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'teacher_password', 'type': 'VARCHAR(100)', 'key': '', 'extra': 'NOT NULL (Hashed)'},
            ]
        },
        {
            'name': 'student',
            'desc': 'Enrolled students with GTU university roll number and active semester.',
            'fields': [
                {'name': 'student_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'student_name', 'type': 'VARCHAR(50)', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'student_email', 'type': 'VARCHAR(50)', 'key': 'UNI', 'extra': 'NOT NULL, UNIQUE'},
                {'name': 'roll_no', 'type': 'VARCHAR(15)', 'key': 'UNI', 'extra': 'NOT NULL, UNIQUE'},
                {'name': 'semester', 'type': 'INT', 'key': '', 'extra': 'NOT NULL (1 - 8)'},
                {'name': 'student_password', 'type': 'VARCHAR(100)', 'key': '', 'extra': 'NOT NULL (Hashed)'},
            ]
        },
        {
            'name': 'course',
            'desc': 'Academic subjects taught in BCA semesters, mapped to assigned professors.',
            'fields': [
                {'name': 'course_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'course_name', 'type': 'VARCHAR(50)', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'teacher_id', 'type': 'INT', 'key': 'FK', 'extra': 'REFERENCES teacher(teacher_id)'},
                {'name': 'semester', 'type': 'INT', 'key': '', 'extra': 'NOT NULL'},
            ]
        },
        {
            'name': 'enrollment',
            'desc': 'Mapping of enrolled students to active courses with enrolment dates.',
            'fields': [
                {'name': 'enroll_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'student_id', 'type': 'INT', 'key': 'FK', 'extra': 'REFERENCES student(student_id)'},
                {'name': 'course_id', 'type': 'INT', 'key': 'FK', 'extra': 'REFERENCES course(course_id)'},
                {'name': 'enroll_date', 'type': 'DATE', 'key': '', 'extra': 'DEFAULT CURRENT_DATE, UNIQUE(student, course)'},
            ]
        },
        {
            'name': 'assignment',
            'desc': 'Tasks created by teachers containing submission deadlines and max marks.',
            'fields': [
                {'name': 'assignment_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'title', 'type': 'VARCHAR(100)', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'description', 'type': 'TEXT', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'course_id', 'type': 'INT', 'key': 'FK', 'extra': 'REFERENCES course(course_id)'},
                {'name': 'due_date', 'type': 'DATETIME', 'key': 'MUL', 'extra': 'NOT NULL (INDEXED)'},
                {'name': 'max_marks', 'type': 'INT', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'file_path', 'type': 'VARCHAR(200)', 'key': '', 'extra': 'NULLABLE (Optional briefing file)'},
            ]
        },
        {
            'name': 'submission',
            'desc': 'File submissions made by students along with timestamp and status tracking.',
            'fields': [
                {'name': 'submission_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'assignment_id', 'type': 'INT', 'key': 'FK', 'extra': 'REFERENCES assignment(assignment_id)'},
                {'name': 'student_id', 'type': 'INT', 'key': 'FK', 'extra': 'REFERENCES student(student_id)'},
                {'name': 'file_path', 'type': 'VARCHAR(200)', 'key': '', 'extra': 'NOT NULL, UNIQUE(assignment, student)'},
                {'name': 'submitted_at', 'type': 'DATETIME', 'key': '', 'extra': 'DEFAULT CURRENT_TIMESTAMP'},
                {'name': 'status', 'type': 'VARCHAR(20)', 'key': '', 'extra': 'Pending/Submitted/Late/Evaluated/Returned'},
            ]
        },
        {
            'name': 'evaluation',
            'desc': 'Grading records and qualitative feedback awarded by teachers.',
            'fields': [
                {'name': 'evaluation_id', 'type': 'INT', 'key': 'PK', 'extra': 'AUTO_INCREMENT'},
                {'name': 'submission_id', 'type': 'INT', 'key': 'UNI/FK', 'extra': 'REFERENCES submission(submission_id) UNIQUE'},
                {'name': 'marks', 'type': 'INT', 'key': '', 'extra': 'NOT NULL (0 to max_marks)'},
                {'name': 'feedback', 'type': 'VARCHAR(250)', 'key': '', 'extra': 'NOT NULL'},
                {'name': 'evaluated_on', 'type': 'DATE', 'key': '', 'extra': 'DEFAULT CURRENT_DATE'},
            ]
        },
    ]
    return render(request, 'public/database.html', {'tables': tables})


def team(request):
    team_members = [
        {'name': 'Dishant Jain', 'roll': '3031', 'role': 'Frontend Architecture & Diagram Design', 'class': 'BCA Sem 5'},
        {'name': 'Mehul Jain', 'roll': '3032', 'role': 'Database Schema & Reports Analytics', 'class': 'BCA Sem 5'},
        {'name': 'Shivang Saluke', 'roll': '3092', 'role': 'Backend Systems & Role Controllers', 'class': 'BCA Sem 5'},
    ]
    return render(request, 'public/team.html', {'members': team_members})


# ==========================================
# AUTHENTICATION & REGISTRATION
# ==========================================

def register_student(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')

    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
        if form.is_valid():
            name = form.cleaned_data['student_name']
            email = form.cleaned_data['student_email']
            roll = form.cleaned_data['roll_no']
            sem = form.cleaned_data['semester']
<<<<<<< HEAD
            pwd = form.cleaned_data['student_password']

            # Check if email or roll number already exists
            if User.objects.filter(email=email).exists() or Student.objects.filter(student_email=email).exists():
                messages.error(request, "A student account with this email already exists.")
                return render(request, 'public/register.html', {'form': form})
            if Student.objects.filter(roll_no=roll).exists():
                messages.error(request, "A student account with this roll number already exists.")
                return render(request, 'public/register.html', {'form': form})

            # Create User
            username = f"std_{roll}"
            user = User.objects.create_user(
                username=username,
                email=email,
                password=pwd,
                first_name=name
            )

=======
            pwd = form.cleaned_data['password']

            # Create User
            user = User.objects.create_user(username=email, email=email, password=pwd, first_name=name)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
            # Create Student profile
            student = Student.objects.create(
                student_name=name,
                student_email=email,
                roll_no=roll,
                semester=sem,
                student_password=user.password,
                user=user
            )

            # Auto-enroll in courses matching their semester
            sem_courses = Course.objects.filter(semester=sem)
            for c in sem_courses:
                Enrollment.objects.get_or_create(student_id=student, course_id=c)

<<<<<<< HEAD
            login(request, user)
            messages.success(request, f"Registration successful! Welcome to SAMS, {name}.")
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
=======
            messages.success(request, f"Registration successful! Welcome to SAMS, {name}. Please log in with your credentials.")
            return redirect('login')
    else:
        form = StudentRegisterForm()
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1

    return render(request, 'public/register.html', {'form': form})


<<<<<<< HEAD
# ========================================================
# ADMIN VIEWS
# ========================================================

@admin_required
def admin_dashboard(request):
    """Admin Overview with system counts and recent activities."""
    courses_count = Course.objects.count()
    teachers_count = Teacher.objects.count()
    students_count = Student.objects.count()
    assignments_count = Assignment.objects.count()
    submissions_count = Submission.objects.count()
    evaluations_count = Evaluation.objects.count()

    # Submission metrics
    late_count = Submission.objects.filter(status='Late').count()
    evaluated_count = Submission.objects.filter(status__in=['Evaluated', 'Returned']).count()
    submission_rate = round((submissions_count / (assignments_count * students_count) * 100), 1) if (assignments_count * students_count) > 0 else 0
    avg_marks = Evaluation.objects.aggregate(avg=Avg('marks'))['avg'] or 0

    recent_submissions = Submission.objects.select_related('student_id', 'assignment_id', 'assignment_id__course_id').order_by('-submitted_at')[:8]

    context = {
        'courses_count': courses_count,
        'teachers_count': teachers_count,
        'students_count': students_count,
        'assignments_count': assignments_count,
        'submissions_count': submissions_count,
        'evaluations_count': evaluations_count,
        'late_count': late_count,
        'evaluated_count': evaluated_count,
        'submission_rate': submission_rate,
        'avg_marks': round(avg_marks, 1),
        'recent_submissions': recent_submissions,
    }
    return render(request, 'admin_panel/dashboard.html', context)
=======
def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if not user:
                try:
                    u_match = User.objects.get(email__iexact=email)
                    user = authenticate(request, username=u_match.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None and Teacher.objects.filter(user=user).exists():
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('teacher_dashboard')
            elif user is not None:
                messages.error(request, "This account does not have faculty teacher permissions.")
            else:
                messages.error(request, "Invalid faculty email or password.")
    else:
        form = LoginForm(initial={'role': 'teacher'})
    return render(request, 'public/login_teacher.html', {'form': form})


def student_login(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if not user:
                try:
                    u_match = User.objects.get(email__iexact=email)
                    user = authenticate(request, username=u_match.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None and Student.objects.filter(user=user).exists():
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('student_dashboard')
            elif user is not None:
                messages.error(request, "This account is not registered as a student.")
            else:
                messages.error(request, "Invalid student email or password.")
    else:
        form = LoginForm(initial={'role': 'student'})
    return render(request, 'public/login_student.html', {'form': form})


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if not user:
                try:
                    u_match = User.objects.get(email__iexact=email)
                    user = authenticate(request, username=u_match.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None and (Admin.objects.filter(user=user).exists() or user.is_superuser):
                login(request, user)
                messages.success(request, f"Welcome, Administrator {user.first_name or user.username}!")
                return redirect('admin_dashboard')
            elif user is not None:
                messages.error(request, "Access restricted to system administrators.")
            else:
                messages.error(request, "Invalid administrator email or password.")
    else:
        form = LoginForm(initial={'role': 'admin'})
    return render(request, 'public/login_admin.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')

    role_param = request.GET.get('role')
    if role_param == 'teacher':
        return teacher_login(request)
    elif role_param == 'admin':
        return admin_login(request)
    elif role_param == 'student':
        return student_login(request)
    # Default landing login is Student Login (clean, dedicated)
    return student_login(request)


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if Admin.objects.filter(user=request.user).exists() or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif Teacher.objects.filter(user=request.user).exists():
        return redirect('teacher_dashboard')
    elif Student.objects.filter(user=request.user).exists():
        return redirect('student_dashboard')

    return redirect('home')


def switch_role(request, role):
    if not request.user.is_authenticated:
        return redirect('login')

    # Security check: ONLY Administrator (or an active Admin impersonator) can switch roles
    is_admin = Admin.objects.filter(user=request.user).exists() or request.user.is_superuser
    is_impersonating = request.session.get('impersonated_by_admin', False)

    if not (is_admin or is_impersonating):
        messages.error(request, "Permission Denied: Only administrators have authority to switch portals without logging out. Teachers and students must sign in with their own credentials.")
        return redirect('login_redirect')

    # If currently an actual admin, store original admin id in session
    if is_admin and not is_impersonating:
        request.session['original_admin_id'] = request.user.id
        request.session['impersonated_by_admin'] = True

    if role == 'admin':
        # Return to original admin account
        admin_id = request.session.get('original_admin_id')
        admin_user = None
        if admin_id:
            admin_user = User.objects.filter(id=admin_id).first()
        if not admin_user:
            admin_obj = Admin.objects.first()
            admin_user = admin_obj.user if admin_obj else User.objects.filter(is_superuser=True).first()

        if admin_user:
            login(request, admin_user)
            # Clear impersonation flags
            request.session.pop('impersonated_by_admin', None)
            request.session.pop('original_admin_id', None)
            messages.success(request, f"Returned to Administrator Desk as {admin_user.first_name or admin_user.username}!")
            return redirect('admin_dashboard')

    elif role == 'teacher':
        teacher_obj = Teacher.objects.first()
        if teacher_obj and teacher_obj.user:
            login(request, teacher_obj.user)
            request.session['impersonated_by_admin'] = True
            messages.success(request, f"Admin viewing as Faculty: Dr. {teacher_obj.teacher_name}!")
            return redirect('teacher_dashboard')

    elif role == 'student':
        student_obj = Student.objects.first()
        if student_obj and student_obj.user:
            login(request, student_obj.user)
            request.session['impersonated_by_admin'] = True
            messages.success(request, f"Admin viewing as Student: {student_obj.student_name}!")
            return redirect('student_dashboard')

    messages.warning(request, f"Could not switch to role '{role}'.")
    return redirect('login_redirect')


# ==========================================
# ADMIN PORTAL
# ==========================================

@admin_required
def admin_dashboard(request):
    counts = {
        'students': Student.objects.count(),
        'teachers': Teacher.objects.count(),
        'courses': Course.objects.count(),
        'assignments': Assignment.objects.count(),
        'submissions': Submission.objects.count(),
        'evaluations': Evaluation.objects.count(),
        'late_submissions': Submission.objects.filter(status='Late').count(),
    }
    recent_submissions = Submission.objects.select_related('assignment_id', 'student_id', 'assignment_id__course_id').order_by('-submitted_at')[:8]
    recent_assignments = Assignment.objects.select_related('course_id', 'course_id__teacher_id').order_by('-due_date')[:6]

    return render(request, 'admin_panel/dashboard.html', {
        'counts': counts,
        'recent_submissions': recent_submissions,
        'recent_assignments': recent_assignments,
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_courses(request):
<<<<<<< HEAD
    """Manage courses list."""
    courses = Course.objects.select_related('teacher_id').annotate(
        students_count=Count('enrollments', distinct=True),
        assignments_count=Count('assignments', distinct=True)
    ).order_by('semester', 'course_name')
    teachers = Teacher.objects.all()
    return render(request, 'admin_panel/courses.html', {'courses': courses, 'teachers': teachers})
=======
    search_q = request.GET.get('q', '').strip()
    sem_filter = request.GET.get('sem', '')
    
    courses = Course.objects.select_related('teacher_id').all().order_by('semester', 'course_name')
    if search_q:
        courses = courses.filter(course_name__icontains=search_q)
    if sem_filter:
        courses = courses.filter(semester=sem_filter)

    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_panel/courses.html', {
        'page_obj': page_obj,
        'search_q': search_q,
        'sem_filter': sem_filter,
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_course_add(request):
<<<<<<< HEAD
    """Add a new course."""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            # Auto enroll existing students of the same semester
            students = Student.objects.filter(semester=course.semester)
            for s in students:
                Enrollment.objects.get_or_create(student_id=s, course_id=course)
            messages.success(request, f"Course '{course.course_name}' created successfully.")
            return redirect('admin_courses')
    else:
        form = CourseForm()
    return render(request, 'admin_panel/course_form.html', {'form': form, 'title': 'Add Course'})
=======
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{form.cleaned_data['course_name']}' created successfully!")
            return redirect('admin_courses')
    else:
        form = CourseForm()
    return render(request, 'admin_panel/course_form.html', {'form': form, 'title': 'Add New Course'})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_course_edit(request, course_id):
<<<<<<< HEAD
    """Edit an existing course."""
=======
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            messages.success(request, f"Course '{course.course_name}' updated.")
            return redirect('admin_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin_panel/course_form.html', {'form': form, 'course': course, 'title': 'Edit Course'})
=======
            messages.success(request, f"Course '{course.course_name}' updated successfully!")
            return redirect('admin_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin_panel/course_form.html', {'form': form, 'title': f'Edit Course: {course.course_name}', 'is_edit': True})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_course_delete(request, course_id):
<<<<<<< HEAD
    """Delete a course."""
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == 'POST':
        name = course.course_name
        course.delete()
        messages.success(request, f"Course '{name}' has been deleted.")
        return redirect('admin_courses')
    return render(request, 'admin_panel/confirm_delete.html', {'item': course, 'type': 'Course', 'back_url': 'admin_courses'})
=======
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == 'POST':
        c_name = course.course_name
        course.delete()
        messages.success(request, f"Course '{c_name}' deleted successfully.")
        return redirect('admin_courses')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object_name': course.course_name,
        'item_type': 'Course',
        'cancel_url': 'admin_courses'
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_teachers(request):
<<<<<<< HEAD
    """Manage teachers list."""
    teachers = Teacher.objects.annotate(courses_count=Count('courses')).order_by('teacher_name')
    return render(request, 'admin_panel/teachers.html', {'teachers': teachers})
=======
    search_q = request.GET.get('q', '').strip()
    teachers = Teacher.objects.prefetch_related('courses').all().order_by('teacher_name')
    if search_q:
        teachers = teachers.filter(Q(teacher_name__icontains=search_q) | Q(department__icontains=search_q) | Q(teacher_email__icontains=search_q))

    paginator = Paginator(teachers, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/teachers.html', {'page_obj': page_obj, 'search_q': search_q})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_teacher_add(request):
<<<<<<< HEAD
    """Register a new teacher."""
=======
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['teacher_email']
            name = form.cleaned_data['teacher_name']
            dept = form.cleaned_data['department']
<<<<<<< HEAD
            pwd = form.cleaned_data['teacher_password']

            if User.objects.filter(email=email).exists() or Teacher.objects.filter(teacher_email=email).exists():
                messages.error(request, "Teacher with this email already exists.")
                return render(request, 'admin_panel/teacher_form.html', {'form': form, 'title': 'Add Teacher'})

            username = email.split('@')[0]
            if User.objects.filter(username=username).exists():
                username = f"{username}_{Teacher.objects.count() + 1}"

            user = User.objects.create_user(username=username, email=email, password=pwd, first_name=name)
            Teacher.objects.create(
                teacher_name=name,
                teacher_email=email,
                department=dept,
                teacher_password=user.password,
                user=user
            )
            messages.success(request, f"Teacher '{name}' added successfully.")
            return redirect('admin_teachers')
    else:
        form = TeacherForm()
    return render(request, 'admin_panel/teacher_form.html', {'form': form, 'title': 'Add Teacher'})
=======
            pwd = form.cleaned_data.get('password') or 'teacher123'

            if User.objects.filter(username=email).exists():
                form.add_error('teacher_email', 'User account already exists with this email.')
            else:
                user = User.objects.create_user(username=email, email=email, password=pwd, first_name=name)
                Teacher.objects.create(
                    teacher_name=name,
                    teacher_email=email,
                    department=dept,
                    teacher_password=user.password,
                    user=user
                )
                messages.success(request, f"Teacher '{name}' added successfully!")
                return redirect('admin_teachers')
    else:
        form = TeacherForm()
    return render(request, 'admin_panel/teacher_form.html', {'form': form, 'title': 'Add Faculty Member'})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_teacher_edit(request, teacher_id):
<<<<<<< HEAD
    """Edit teacher details."""
=======
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
<<<<<<< HEAD
            t = form.save(commit=False)
            pwd = form.cleaned_data['teacher_password']
            if pwd and not pwd.startswith('pbkdf2_'):
                if teacher.user:
                    teacher.user.set_password(pwd)
                    teacher.user.save()
                    t.teacher_password = teacher.user.password
            t.save()
            if teacher.user:
                teacher.user.email = t.teacher_email
                teacher.user.first_name = t.teacher_name
                teacher.user.save()
            messages.success(request, f"Teacher '{teacher.teacher_name}' updated.")
            return redirect('admin_teachers')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'admin_panel/teacher_form.html', {'form': form, 'teacher': teacher, 'title': 'Edit Teacher'})
=======
            teacher = form.save(commit=False)
            pwd = form.cleaned_data.get('password')
            if pwd and teacher.user:
                teacher.user.set_password(pwd)
                teacher.user.save()
                teacher.teacher_password = teacher.user.password
            teacher.save()
            messages.success(request, f"Teacher '{teacher.teacher_name}' updated successfully!")
            return redirect('admin_teachers')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'admin_panel/teacher_form.html', {'form': form, 'title': f'Edit Teacher: {teacher.teacher_name}', 'is_edit': True})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_teacher_delete(request, teacher_id):
<<<<<<< HEAD
    """Delete teacher account."""
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        name = teacher.teacher_name
        if teacher.user:
            teacher.user.delete()
        else:
            teacher.delete()
        messages.success(request, f"Teacher '{name}' deleted.")
        return redirect('admin_teachers')
    return render(request, 'admin_panel/confirm_delete.html', {'item': teacher, 'type': 'Teacher', 'back_url': 'admin_teachers'})
=======
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        t_name = teacher.teacher_name
        if teacher.user:
            teacher.user.delete()
        teacher.delete()
        messages.success(request, f"Teacher '{t_name}' removed.")
        return redirect('admin_teachers')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object_name': teacher.teacher_name,
        'item_type': 'Teacher',
        'cancel_url': 'admin_teachers'
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_students(request):
<<<<<<< HEAD
    """Manage students list."""
    students = Student.objects.annotate(
        enrollments_count=Count('enrollments', distinct=True),
        submissions_count=Count('submissions', distinct=True)
    ).order_by('semester', 'roll_no')
    return render(request, 'admin_panel/students.html', {'students': students})
=======
    search_q = request.GET.get('q', '').strip()
    sem_filter = request.GET.get('sem', '')
    students = Student.objects.prefetch_related('enrollments__course_id').all().order_by('roll_no')
    if search_q:
        students = students.filter(Q(student_name__icontains=search_q) | Q(roll_no__icontains=search_q) | Q(student_email__icontains=search_q))
    if sem_filter:
        students = students.filter(semester=sem_filter)

    paginator = Paginator(students, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/students.html', {'page_obj': page_obj, 'search_q': search_q, 'sem_filter': sem_filter})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_student_add(request):
<<<<<<< HEAD
    """Add a new student."""
    if request.method == 'POST':
        form = StudentAdminForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['student_name']
            email = form.cleaned_data['student_email']
            roll = form.cleaned_data['roll_no']
            sem = form.cleaned_data['semester']
            pwd = form.cleaned_data['student_password']

            if User.objects.filter(email=email).exists() or Student.objects.filter(student_email=email).exists():
                messages.error(request, "Student with this email already exists.")
                return render(request, 'admin_panel/student_form.html', {'form': form, 'title': 'Add Student'})
            if Student.objects.filter(roll_no=roll).exists():
                messages.error(request, "Student with this roll number already exists.")
                return render(request, 'admin_panel/student_form.html', {'form': form, 'title': 'Add Student'})

            username = f"std_{roll}"
            user = User.objects.create_user(username=username, email=email, password=pwd, first_name=name)
            student = Student.objects.create(
                student_name=name,
                student_email=email,
                roll_no=roll,
                semester=sem,
                student_password=user.password,
                user=user
            )

            # Auto-enroll in courses
            for c in Course.objects.filter(semester=sem):
                Enrollment.objects.get_or_create(student_id=student, course_id=c)

            messages.success(request, f"Student '{name}' added successfully.")
            return redirect('admin_students')
=======
    if request.method == 'POST':
        form = StudentAdminForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['student_email']
            name = form.cleaned_data['student_name']
            roll = form.cleaned_data['roll_no']
            sem = form.cleaned_data['semester']
            pwd = form.cleaned_data.get('password') or 'student123'

            if User.objects.filter(username=email).exists():
                form.add_error('student_email', 'User account exists with this email.')
            elif Student.objects.filter(roll_no=roll).exists():
                form.add_error('roll_no', 'Roll number already exists.')
            else:
                user = User.objects.create_user(username=email, email=email, password=pwd, first_name=name)
                student = Student.objects.create(
                    student_name=name,
                    student_email=email,
                    roll_no=roll,
                    semester=sem,
                    student_password=user.password,
                    user=user
                )
                # Auto-enroll in semester courses
                sem_courses = Course.objects.filter(semester=sem)
                for c in sem_courses:
                    Enrollment.objects.get_or_create(student_id=student, course_id=c)

                messages.success(request, f"Student '{name}' ({roll}) enrolled successfully!")
                return redirect('admin_students')
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    else:
        form = StudentAdminForm()
    return render(request, 'admin_panel/student_form.html', {'form': form, 'title': 'Add Student'})


@admin_required
def admin_student_edit(request, student_id):
<<<<<<< HEAD
    """Edit student profile."""
=======
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = StudentAdminForm(request.POST, instance=student)
        if form.is_valid():
<<<<<<< HEAD
            s = form.save(commit=False)
            pwd = form.cleaned_data['student_password']
            if pwd and not pwd.startswith('pbkdf2_'):
                if student.user:
                    student.user.set_password(pwd)
                    student.user.save()
                    s.student_password = student.user.password
            s.save()
            if student.user:
                student.user.email = s.student_email
                student.user.first_name = s.student_name
                student.user.save()
            messages.success(request, f"Student '{student.student_name}' updated.")
            return redirect('admin_students')
    else:
        form = StudentAdminForm(instance=student)
    return render(request, 'admin_panel/student_form.html', {'form': form, 'student': student, 'title': 'Edit Student'})
=======
            student = form.save(commit=False)
            pwd = form.cleaned_data.get('password')
            if pwd and student.user:
                student.user.set_password(pwd)
                student.user.save()
                student.student_password = student.user.password
            student.save()
            messages.success(request, f"Student '{student.student_name}' updated successfully!")
            return redirect('admin_students')
    else:
        form = StudentAdminForm(instance=student)
    return render(request, 'admin_panel/student_form.html', {'form': form, 'title': f'Edit Student: {student.student_name}', 'is_edit': True})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_student_delete(request, student_id):
<<<<<<< HEAD
    """Delete student account."""
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        name = student.student_name
        if student.user:
            student.user.delete()
        else:
            student.delete()
        messages.success(request, f"Student '{name}' deleted.")
        return redirect('admin_students')
    return render(request, 'admin_panel/confirm_delete.html', {'item': student, 'type': 'Student', 'back_url': 'admin_students'})
=======
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        s_name = student.student_name
        if student.user:
            student.user.delete()
        student.delete()
        messages.success(request, f"Student '{s_name}' removed.")
        return redirect('admin_students')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object_name': f"{student.student_name} ({student.roll_no})",
        'item_type': 'Student',
        'cancel_url': 'admin_students'
    })


@admin_required
def admin_enrollments(request):
    search_q = request.GET.get('q', '').strip()
    enrollments = Enrollment.objects.select_related('student_id', 'course_id', 'course_id__teacher_id').all().order_by('-enroll_date')
    if search_q:
        enrollments = enrollments.filter(
            Q(student_id__student_name__icontains=search_q) |
            Q(student_id__roll_no__icontains=search_q) |
            Q(course_id__course_name__icontains=search_q)
        )

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student enrolled in course successfully!")
                return redirect('admin_enrollments')
            except Exception as e:
                messages.error(request, "This student is already enrolled in that course.")
    else:
        form = EnrollmentForm()

    paginator = Paginator(enrollments, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/enrollments.html', {'page_obj': page_obj, 'form': form, 'search_q': search_q})


@admin_required
def admin_enrollment_delete(request, enroll_id):
    enrollment = get_object_or_404(Enrollment, enroll_id=enroll_id)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, "Enrolment record removed.")
        return redirect('admin_enrollments')
    return render(request, 'admin_panel/confirm_delete.html', {
        'object_name': f"{enrollment.student_id.student_name} in {enrollment.course_id.course_name}",
        'item_type': 'Enrollment',
        'cancel_url': 'admin_enrollments'
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_assignments(request):
<<<<<<< HEAD
    """Monitor all assignments and overall submissions across the portal."""
    assignments = Assignment.objects.select_related('course_id', 'course_id__teacher_id').annotate(
        total_subs=Count('submissions', distinct=True)
    ).order_by('-due_date')
    return render(request, 'admin_panel/assignments.html', {'assignments': assignments})
=======
    search_q = request.GET.get('q', '').strip()
    assignments = Assignment.objects.select_related('course_id', 'course_id__teacher_id').annotate(
        submission_count=Count('submissions')
    ).order_by('-due_date')
    if search_q:
        assignments = assignments.filter(Q(title__icontains=search_q) | Q(course_id__course_name__icontains=search_q))

    paginator = Paginator(assignments, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/assignments.html', {'page_obj': page_obj, 'search_q': search_q})


@admin_required
def admin_submissions(request):
    filter_status = request.GET.get('status', '')
    course_filter = request.GET.get('course', '')
    submissions = Submission.objects.select_related('assignment_id', 'student_id', 'assignment_id__course_id', 'evaluation').order_by('-submitted_at')

    if filter_status:
        if filter_status == 'pending':
            submissions = submissions.filter(evaluation__isnull=True)
        else:
            submissions = submissions.filter(status=filter_status)
    if course_filter:
        submissions = submissions.filter(assignment_id__course_id_id=course_filter)

    courses = Course.objects.all()
    paginator = Paginator(submissions, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'admin_panel/submissions.html', {
        'page_obj': page_obj,
        'filter_status': filter_status,
        'course_filter': course_filter,
        'courses': courses,
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_reports(request):
<<<<<<< HEAD
    """Analytics and reporting dashboard."""
    total_assignments = Assignment.objects.count()
    total_submissions = Submission.objects.count()
    total_students = Student.objects.count()

    late_count = Submission.objects.filter(status='Late').count()
    on_time_count = Submission.objects.filter(status='Submitted').count()
    evaluated_count = Submission.objects.filter(status__in=['Evaluated', 'Returned']).count()

    overall_submission_rate = round((total_submissions / (total_assignments * total_students) * 100), 1) if (total_assignments * total_students) > 0 else 0
    avg_marks = Evaluation.objects.aggregate(avg=Avg('marks'))['avg'] or 0

    course_stats = Course.objects.annotate(
        assign_count=Count('assignments', distinct=True),
        sub_count=Count('assignments__submissions', distinct=True),
        student_count=Count('enrollments', distinct=True)
    )

    context = {
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'late_count': late_count,
        'on_time_count': on_time_count,
        'evaluated_count': evaluated_count,
        'overall_submission_rate': overall_submission_rate,
        'avg_marks': round(avg_marks, 1),
        'course_stats': course_stats,
    }
    return render(request, 'admin_panel/reports.html', context)
=======
    # 1. Course performance analytics
    courses = Course.objects.annotate(
        total_assignments=Count('assignments', distinct=True),
        total_students=Count('enrollments', distinct=True),
    )

    course_analytics = []
    course_names = []
    submission_rates = []
    avg_marks_list = []

    for c in courses:
        total_submissions = Submission.objects.filter(assignment_id__course_id=c).count()
        total_expected = c.total_assignments * c.total_students
        rate = round((total_submissions / total_expected * 100), 1) if total_expected > 0 else 0
        
        avg_score = Evaluation.objects.filter(submission_id__assignment_id__course_id=c).aggregate(Avg('marks'))['marks__avg']
        avg_score = round(avg_score, 1) if avg_score else 0

        late_subs = Submission.objects.filter(assignment_id__course_id=c, status='Late').count()

        course_analytics.append({
            'course': c,
            'rate': rate,
            'total_submissions': total_submissions,
            'expected_submissions': total_expected,
            'avg_marks': avg_score,
            'late_count': late_subs,
        })
        course_names.append(c.course_name)
        submission_rates.append(rate)
        avg_marks_list.append(avg_score)

    # 2. Global status breakdown
    status_counts = {
        'Submitted': Submission.objects.filter(status='Submitted').count(),
        'Late': Submission.objects.filter(status='Late').count(),
        'Evaluated': Submission.objects.filter(status__in=['Evaluated', 'Returned']).count(),
    }

    return render(request, 'admin_panel/reports.html', {
        'course_analytics': course_analytics,
        'course_names_json': json.dumps(course_names),
        'submission_rates_json': json.dumps(submission_rates),
        'avg_marks_json': json.dumps(avg_marks_list),
        'status_counts': status_counts,
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@admin_required
def admin_profile(request):
<<<<<<< HEAD
    """Admin profile details."""
    admin_obj = getattr(request.user, 'admin_profile', None)
    return render(request, 'admin_panel/profile.html', {'admin_obj': admin_obj})


# ========================================================
# TEACHER VIEWS
# ========================================================

@teacher_required
def teacher_dashboard(request):
    """Teacher Overview with pending reviews and own courses."""
    teacher = request.user.teacher_profile
    courses = Course.objects.filter(teacher_id=teacher)
    assignments = Assignment.objects.filter(course_id__in=courses)

    submissions_pending = Submission.objects.filter(
        assignment_id__in=assignments,
        status__in=['Submitted', 'Late']
    ).select_related('student_id', 'assignment_id').order_by('-submitted_at')

    evaluated_count = Submission.objects.filter(
        assignment_id__in=assignments,
        status__in=['Evaluated', 'Returned']
    ).count()

    context = {
        'teacher': teacher,
        'courses': courses,
        'assignments': assignments,
        'pending_submissions': submissions_pending[:6],
        'pending_count': submissions_pending.count(),
        'evaluated_count': evaluated_count,
        'total_assignments': assignments.count(),
    }
    return render(request, 'teacher/dashboard.html', context)
=======
    admin_obj = Admin.objects.filter(user=request.user).first()
    return render(request, 'admin_panel/profile.html', {'admin_obj': admin_obj})


# ==========================================
# TEACHER PORTAL
# ==========================================

@teacher_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(teacher_id=teacher)
    
    total_courses = courses.count()
    assignments = Assignment.objects.filter(course_id__in=courses)
    total_assignments = assignments.count()
    
    submissions = Submission.objects.filter(assignment_id__in=assignments)
    total_submissions = submissions.count()
    pending_evaluations = submissions.filter(evaluation__isnull=True).count()
    evaluated_count = submissions.filter(evaluation__isnull=False).count()

    recent_submissions = submissions.select_related('student_id', 'assignment_id', 'evaluation').order_by('-submitted_at')[:8]
    upcoming_deadlines = assignments.filter(due_date__gte=timezone.now()).order_by('due_date')[:5]

    return render(request, 'teacher/dashboard.html', {
        'teacher': teacher,
        'courses': courses,
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'total_submissions': total_submissions,
        'pending_evaluations': pending_evaluations,
        'evaluated_count': evaluated_count,
        'recent_submissions': recent_submissions,
        'upcoming_deadlines': upcoming_deadlines,
    })


@teacher_required
def teacher_courses(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(teacher_id=teacher).annotate(
        student_count=Count('enrollments', distinct=True),
        assignment_count=Count('assignments', distinct=True)
    )
    return render(request, 'teacher/courses.html', {'courses': courses})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@teacher_required
def teacher_assignments(request):
<<<<<<< HEAD
    """List and manage teacher's own assignments."""
    teacher = request.user.teacher_profile
    courses = Course.objects.filter(teacher_id=teacher)
    assignments = Assignment.objects.filter(course_id__in=courses).select_related('course_id').annotate(
        subs_count=Count('submissions')
    ).order_by('-due_date')

    return render(request, 'teacher/assignments.html', {'assignments': assignments, 'courses': courses})


@teacher_required
def teacher_assignment_create(request):
    """Create a new assignment for teacher's own course."""
    teacher = request.user.teacher_profile
    courses = Course.objects.filter(teacher_id=teacher)

    if not courses.exists():
        messages.warning(request, "You have not been assigned any courses yet. Please contact the administrator.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        # Limit course choices to teacher's courses
        form.fields['course_id'].queryset = courses
        if form.is_valid():
            assignment = form.save(commit=False)
            # Handle optional attachment file
            if 'attachment' in request.FILES:
                file_obj = request.FILES['attachment']
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'assignments', str(assignment.course_id.course_id))
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join('assignments', str(assignment.course_id.course_id), file_obj.name)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                with open(full_path, 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                assignment.file_path = file_path
            assignment.save()
            messages.success(request, f"Assignment '{assignment.title}' created successfully.")
            return redirect('teacher_assignments')
    else:
        form = AssignmentForm()
        form.fields['course_id'].queryset = courses

    return render(request, 'teacher/assignment_form.html', {'form': form, 'title': 'Create Assignment'})
=======
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(teacher_id=teacher)
    
    assignments = Assignment.objects.filter(course_id__teacher_id=teacher).select_related('course_id').annotate(
        submission_count=Count('submissions')
    ).order_by('-due_date')

    # Filter by course
    selected_course_id = request.GET.get('course')
    if selected_course_id:
        assignments = assignments.filter(course_id_id=selected_course_id)

    # Search by title or description
    search_q = request.GET.get('q', '').strip()
    if search_q:
        assignments = assignments.filter(
            Q(title__icontains=search_q) | Q(description__icontains=search_q)
        )

    all_teacher_assignments_count = Assignment.objects.filter(course_id__teacher_id=teacher).count()

    paginator = Paginator(assignments, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'teacher/assignment_list.html', {
        'page_obj': page_obj,
        'courses': courses,
        'selected_course_id': selected_course_id,
        'search_q': search_q,
        'total_count': all_teacher_assignments_count,
    })


@teacher_required
def teacher_assignment_add(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        # Limit course choices to this teacher's courses
        form.fields['course_id'].queryset = Course.objects.filter(teacher_id=teacher)
        if form.is_valid():
            assignment = form.save(commit=False)
            attachment = form.cleaned_data.get('attachment')
            if attachment:
                # Save attachment
                rel_dir = os.path.join('assignments', str(assignment.course_id.course_id))
                full_dir = os.path.join(settings.MEDIA_ROOT, rel_dir)
                os.makedirs(full_dir, exist_ok=True)
                file_dest = os.path.join(full_dir, attachment.name)
                with open(file_dest, 'wb+') as destination:
                    for chunk in attachment.chunks():
                        destination.write(chunk)
                assignment.file_path = f"{rel_dir}/{attachment.name}".replace('\\', '/')
            assignment.save()
            messages.success(request, f"Assignment '{assignment.title}' created successfully!")
            return redirect('teacher_assignments')
    else:
        initial_data = {}
        course_param = request.GET.get('course')
        if course_param:
            initial_data['course_id'] = course_param
        form = AssignmentForm(initial=initial_data)
        form.fields['course_id'].queryset = Course.objects.filter(teacher_id=teacher)
    return render(request, 'teacher/assignment_form.html', {'form': form, 'title': 'Create New Assignment'})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@teacher_required
def teacher_assignment_edit(request, assignment_id):
<<<<<<< HEAD
    """Edit assignment details."""
    teacher = request.user.teacher_profile
    courses = Course.objects.filter(teacher_id=teacher)
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id, course_id__in=courses)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        form.fields['course_id'].queryset = courses
        if form.is_valid():
            assign = form.save(commit=False)
            if 'attachment' in request.FILES:
                file_obj = request.FILES['attachment']
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'assignments', str(assign.course_id.course_id))
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join('assignments', str(assign.course_id.course_id), file_obj.name)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                with open(full_path, 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        destination.write(chunk)
                assign.file_path = file_path
            assign.save()
            messages.success(request, f"Assignment '{assignment.title}' updated.")
            return redirect('teacher_assignments')
    else:
        form = AssignmentForm(instance=assignment)
        form.fields['course_id'].queryset = courses

    return render(request, 'teacher/assignment_form.html', {'form': form, 'assignment': assignment, 'title': 'Edit Assignment'})
=======
    teacher = Teacher.objects.get(user=request.user)
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id, course_id__teacher_id=teacher)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        form.fields['course_id'].queryset = Course.objects.filter(teacher_id=teacher)
        if form.is_valid():
            assignment = form.save(commit=False)
            attachment = form.cleaned_data.get('attachment')
            if attachment:
                rel_dir = os.path.join('assignments', str(assignment.course_id.course_id))
                full_dir = os.path.join(settings.MEDIA_ROOT, rel_dir)
                os.makedirs(full_dir, exist_ok=True)
                file_dest = os.path.join(full_dir, attachment.name)
                with open(file_dest, 'wb+') as destination:
                    for chunk in attachment.chunks():
                        destination.write(chunk)
                assignment.file_path = f"{rel_dir}/{attachment.name}".replace('\\', '/')
            assignment.save()
            messages.success(request, f"Assignment '{assignment.title}' updated successfully!")
            return redirect('teacher_assignments')
    else:
        form = AssignmentForm(instance=assignment)
        form.fields['course_id'].queryset = Course.objects.filter(teacher_id=teacher)
    return render(request, 'teacher/assignment_form.html', {'form': form, 'title': f'Edit: {assignment.title}', 'is_edit': True, 'assignment': assignment})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@teacher_required
def teacher_assignment_delete(request, assignment_id):
<<<<<<< HEAD
    """Delete an assignment."""
    teacher = request.user.teacher_profile
=======
    teacher = Teacher.objects.get(user=request.user)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id, course_id__teacher_id=teacher)
    if request.method == 'POST':
        title = assignment.title
        assignment.delete()
        messages.success(request, f"Assignment '{title}' deleted.")
        return redirect('teacher_assignments')
<<<<<<< HEAD
    return render(request, 'admin_panel/confirm_delete.html', {'item': assignment, 'type': 'Assignment', 'back_url': 'teacher_assignments'})


@teacher_required
def teacher_submissions(request):
    """View and filter submissions across teacher's assignments."""
    teacher = request.user.teacher_profile
    courses = Course.objects.filter(teacher_id=teacher)
    assignments = Assignment.objects.filter(course_id__in=courses)

    status_filter = request.GET.get('status', 'all')
    assignment_filter = request.GET.get('assignment', 'all')

    submissions = Submission.objects.filter(assignment_id__in=assignments).select_related(
        'student_id', 'assignment_id', 'assignment_id__course_id', 'evaluation'
    )

    if status_filter != 'all':
        submissions = submissions.filter(status=status_filter)
    if assignment_filter != 'all':
        submissions = submissions.filter(assignment_id=assignment_filter)

    submissions = submissions.order_by('-submitted_at')

    context = {
        'submissions': submissions,
        'assignments': assignments,
        'current_status': status_filter,
        'current_assignment': assignment_filter,
    }
    return render(request, 'teacher/submissions.html', context)


@teacher_required
def teacher_evaluate(request, submission_id):
    """Evaluate submission, award marks, write feedback."""
    teacher = request.user.teacher_profile
    submission = get_object_or_404(
        Submission.objects.select_related('student_id', 'assignment_id', 'assignment_id__course_id'),
        submission_id=submission_id,
        assignment_id__course_id__teacher_id=teacher
    )

=======
    return render(request, 'teacher/confirm_delete.html', {
        'object_name': assignment.title,
        'item_type': 'Assignment',
        'cancel_url': 'teacher_assignments'
    })


@teacher_required
def teacher_assignment_submissions(request, assignment_id):
    teacher = Teacher.objects.get(user=request.user)
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id, course_id__teacher_id=teacher)
    
    # All students enrolled in this course
    enrolled_students = Student.objects.filter(enrollments__course_id=assignment.course_id)
    # Existing submissions
    submissions = {s.student_id_id: s for s in Submission.objects.filter(assignment_id=assignment).select_related('student_id', 'evaluation')}
    
    # Compile complete roster: submitted, late, pending
    roster = []
    submitted_count = 0
    late_count = 0
    pending_count = 0

    for st in enrolled_students:
        sub = submissions.get(st.student_id)
        if sub:
            if sub.status == 'Late':
                late_count += 1
            else:
                submitted_count += 1
            roster.append({
                'student': st,
                'submission': sub,
                'status': sub.status,
                'submitted_at': sub.submitted_at,
                'evaluation': getattr(sub, 'evaluation', None),
            })
        else:
            pending_count += 1
            roster.append({
                'student': st,
                'submission': None,
                'status': 'Pending',
                'submitted_at': None,
                'evaluation': None,
            })

    return render(request, 'teacher/submissions_list.html', {
        'assignment': assignment,
        'roster': roster,
        'submitted_count': submitted_count,
        'late_count': late_count,
        'pending_count': pending_count,
    })


@teacher_required
def teacher_grade_submission(request, submission_id):
    teacher = Teacher.objects.get(user=request.user)
    submission = get_object_or_404(Submission, submission_id=submission_id, assignment_id__course_id__teacher_id=teacher)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    evaluation = getattr(submission, 'evaluation', None)

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation, max_marks=submission.assignment_id.max_marks)
        if form.is_valid():
            eval_obj = form.save(commit=False)
            eval_obj.submission_id = submission
            eval_obj.evaluated_on = timezone.now().date()
            eval_obj.save()

            # Update submission status to Evaluated
            submission.status = 'Evaluated'
            submission.save()

<<<<<<< HEAD
            messages.success(request, f"Evaluation saved for {submission.student_id.student_name}: {eval_obj.marks}/{submission.assignment_id.max_marks} marks.")
            return redirect('teacher_submissions')
    else:
        form = EvaluationForm(instance=evaluation, max_marks=submission.assignment_id.max_marks)

    context = {
        'submission': submission,
        'evaluation': evaluation,
        'form': form,
    }
    return render(request, 'teacher/evaluate.html', context)
=======
            messages.success(request, f"Submission by {submission.student_id.student_name} graded: {eval_obj.marks}/{submission.assignment_id.max_marks} marks.")
            return redirect('teacher_assignment_submissions', assignment_id=submission.assignment_id.assignment_id)
    else:
        form = EvaluationForm(instance=evaluation, max_marks=submission.assignment_id.max_marks)

    return render(request, 'teacher/grade_submission.html', {
        'submission': submission,
        'form': form,
        'evaluation': evaluation,
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@teacher_required
def teacher_announcements(request):
<<<<<<< HEAD
    """Teacher announcements / notices broadcast."""
    teacher = request.user.teacher_profile
    courses = Course.objects.filter(teacher_id=teacher)
    return render(request, 'teacher/announcements.html', {'teacher': teacher, 'courses': courses})


@teacher_required
def teacher_profile(request):
    """Teacher profile view."""
    teacher = request.user.teacher_profile
    return render(request, 'teacher/profile.html', {'teacher': teacher})


# ========================================================
# STUDENT VIEWS
# ========================================================

@student_required
def student_dashboard(request):
    """Student Overview with enrolled courses, pending work, and recent marks."""
    student = request.user.student_profile
    enrollments = Enrollment.objects.filter(student_id=student).select_related('course_id', 'course_id__teacher_id')
    courses = [e.course_id for e in enrollments]

    assignments = Assignment.objects.filter(course_id__in=courses).select_related('course_id')
    submissions = Submission.objects.filter(student_id=student).select_related('assignment_id', 'evaluation')

    submission_dict = {s.assignment_id.assignment_id: s for s in submissions}

    upcoming = []
    for a in assignments:
        sub = submission_dict.get(a.assignment_id)
        if not sub and not a.is_past_due:
            upcoming.append(a)

    recent_evaluations = [s for s in submissions if s.status in ['Evaluated', 'Returned']][:5]

    context = {
        'student': student,
        'enrollments': enrollments,
        'upcoming_assignments': upcoming[:5],
        'total_enrolled': len(courses),
        'total_submitted': submissions.count(),
        'recent_evaluations': recent_evaluations,
    }
    return render(request, 'student/dashboard.html', context)
=======
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, teacher=teacher)
        if form.is_valid():
            c = form.cleaned_data['course']
            title = form.cleaned_data['title']
            msg = form.cleaned_data['message']
            # We can broadcast notice via messages and flash to enrolled students
            messages.success(request, f"Announcement broadcasted to students enrolled in '{c.course_name}'!")
            return redirect('teacher_announcements')
    else:
        form = AnnouncementForm(teacher=teacher)
    
    courses = Course.objects.filter(teacher_id=teacher)
    return render(request, 'teacher/announcements.html', {'form': form, 'courses': courses})


@teacher_required
def teacher_submissions(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(teacher_id=teacher)

    submissions = Submission.objects.filter(
        assignment_id__course_id__teacher_id=teacher
    ).select_related('student_id', 'assignment_id', 'assignment_id__course_id', 'evaluation').order_by('-submitted_at')

    # Filter by course
    selected_course_id = request.GET.get('course')
    if selected_course_id:
        submissions = submissions.filter(assignment_id__course_id_id=selected_course_id)

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'pending':
        submissions = submissions.filter(evaluation__isnull=True)
    elif status_filter == 'evaluated':
        submissions = submissions.filter(evaluation__isnull=False)
    elif status_filter == 'late':
        submissions = submissions.filter(status='Late')

    # Search by student name, roll number, or assignment title
    search_q = request.GET.get('q', '').strip()
    if search_q:
        submissions = submissions.filter(
            Q(student_id__student_name__icontains=search_q) |
            Q(student_id__roll_no__icontains=search_q) |
            Q(assignment_id__title__icontains=search_q)
        )

    # Status counts for filter pills
    base_subs = Submission.objects.filter(assignment_id__course_id__teacher_id=teacher)
    if selected_course_id:
        base_subs = base_subs.filter(assignment_id__course_id_id=selected_course_id)
    pending_count = base_subs.filter(evaluation__isnull=True).count()
    evaluated_count = base_subs.filter(evaluation__isnull=False).count()
    late_count = base_subs.filter(status='Late').count()
    total_count = base_subs.count()

    paginator = Paginator(submissions, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'teacher/submissions.html', {
        'page_obj': page_obj,
        'courses': courses,
        'selected_course_id': selected_course_id,
        'status_filter': status_filter,
        'search_q': search_q,
        'pending_count': pending_count,
        'evaluated_count': evaluated_count,
        'late_count': late_count,
        'total_count': total_count,
    })


@teacher_required
def teacher_students(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(teacher_id=teacher)

    enrollments = Enrollment.objects.filter(
        course_id__teacher_id=teacher
    ).select_related('student_id', 'course_id')

    selected_course_id = request.GET.get('course')
    if selected_course_id:
        enrollments = enrollments.filter(course_id_id=selected_course_id)

    search_q = request.GET.get('q', '').strip()
    if search_q:
        enrollments = enrollments.filter(
            Q(student_id__student_name__icontains=search_q) |
            Q(student_id__roll_no__icontains=search_q)
        )

    enrollments = enrollments.order_by('course_id__course_name', 'student_id__roll_no')
    paginator = Paginator(enrollments, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'teacher/students.html', {
        'page_obj': page_obj,
        'courses': courses,
        'selected_course_id': selected_course_id,
        'search_q': search_q,
        'total_count': Enrollment.objects.filter(course_id__teacher_id=teacher).count(),
    })


# ==========================================
# STUDENT PORTAL
# ==========================================

@student_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    enrolled_courses = Course.objects.filter(enrollments__student_id=student).select_related('teacher_id')
    
    # Assignments for enrolled courses
    course_assignments = Assignment.objects.filter(course_id__in=enrolled_courses).select_related('course_id')
    
    # My submissions map
    submissions = {s.assignment_id_id: s for s in Submission.objects.filter(student_id=student).select_related('evaluation')}
    
    pending_assignments = []
    submitted_assignments = []
    now = timezone.now()

    for a in course_assignments:
        sub = submissions.get(a.assignment_id)
        if sub:
            submitted_assignments.append({'assignment': a, 'submission': sub})
        else:
            pending_assignments.append(a)

    recent_evaluations = Evaluation.objects.filter(submission_id__student_id=student).select_related('submission_id__assignment_id').order_by('-evaluated_on')[:5]

    return render(request, 'student/dashboard.html', {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'pending_assignments': pending_assignments,
        'submitted_assignments': submitted_assignments,
        'recent_evaluations': recent_evaluations,
        'now': now,
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@student_required
def student_courses(request):
<<<<<<< HEAD
    """View enrolled courses and assigned teachers."""
    student = request.user.student_profile
    enrollments = Enrollment.objects.filter(student_id=student).select_related('course_id', 'course_id__teacher_id')
    return render(request, 'student/courses.html', {'enrollments': enrollments})
=======
    student = Student.objects.get(user=request.user)
    enrolled_courses = Course.objects.filter(enrollments__student_id=student).select_related('teacher_id').annotate(
        assignment_count=Count('assignments')
    )
    return render(request, 'student/courses.html', {'courses': enrolled_courses})
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@student_required
def student_assignments(request):
<<<<<<< HEAD
    """View all assignments from enrolled courses and submission status."""
    student = request.user.student_profile
    courses = Course.objects.filter(enrollments__student_id=student)
    assignments = Assignment.objects.filter(course_id__in=courses).select_related('course_id', 'course_id__teacher_id').order_by('-due_date')

    submissions = Submission.objects.filter(student_id=student).select_related('evaluation')
    sub_map = {s.assignment_id.assignment_id: s for s in submissions}

    assignment_data = []
    for a in assignments:
        sub = sub_map.get(a.assignment_id)
        assignment_data.append({
            'assignment': a,
            'submission': sub,
            'can_submit': (not sub or timezone.now() <= a.due_date) and (not sub or sub.status not in ['Evaluated', 'Returned']),
            'can_resubmit': sub and timezone.now() <= a.due_date and sub.status not in ['Evaluated', 'Returned'],
=======
    student = Student.objects.get(user=request.user)
    enrolled_courses = Course.objects.filter(enrollments__student_id=student)
    assignments = Assignment.objects.filter(course_id__in=enrolled_courses).select_related('course_id', 'course_id__teacher_id').order_by('due_date')

    submissions = {s.assignment_id_id: s for s in Submission.objects.filter(student_id=student).select_related('evaluation')}
    
    assignment_data = []
    for a in assignments:
        sub = submissions.get(a.assignment_id)
        assignment_data.append({
            'assignment': a,
            'submission': sub,
            'is_submitted': sub is not None,
            'is_past_due': timezone.now() > a.due_date,
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
        })

    return render(request, 'student/assignments.html', {'assignment_data': assignment_data})


@student_required
def student_submit(request, assignment_id):
<<<<<<< HEAD
    """Upload assignment submission or resubmit before deadline."""
    student = request.user.student_profile
    courses = Course.objects.filter(enrollments__student_id=student)
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id, course_id__in=courses)

    existing_sub = Submission.objects.filter(assignment_id=assignment, student_id=student).first()

    # Rule: Once evaluated, cannot resubmit
    if existing_sub and existing_sub.status in ['Evaluated', 'Returned']:
        messages.warning(request, "This assignment has already been evaluated and cannot be modified.")
        return redirect('student_submissions')

    # Rule: Past due date cannot resubmit if already submitted
    if existing_sub and timezone.now() > assignment.due_date:
        messages.warning(request, "Deadline has passed. Existing submission cannot be replaced.")
        return redirect('student_submissions')
=======
    student = Student.objects.get(user=request.user)
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)

    # Check if student is enrolled in this course
    if not Enrollment.objects.filter(student_id=student, course_id=assignment.course_id).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    existing_sub = Submission.objects.filter(assignment_id=assignment, student_id=student).first()

    # If evaluated, resubmission is locked
    if existing_sub and hasattr(existing_sub, 'evaluation'):
        messages.warning(request, "This assignment has already been evaluated. Resubmission is closed.")
        return redirect('student_submission_view', submission_id=existing_sub.submission_id)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1

    if request.method == 'POST':
        form = SubmissionUploadForm(request.POST, request.FILES)
        if form.is_valid():
<<<<<<< HEAD
            f = form.cleaned_data['submission_file']
            course_id = assignment.course_id.course_id

            # Save file to media/submissions/<course>/<assignment>/
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'submissions', str(course_id), str(assignment_id))
            os.makedirs(upload_dir, exist_ok=True)
            saved_file_name = f"{student.roll_no}_{f.name}"
            file_rel_path = os.path.join('submissions', str(course_id), str(assignment_id), saved_file_name)
            full_path = os.path.join(settings.MEDIA_ROOT, file_rel_path)

            with open(full_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)

            # Determine status: Late if submitted after due_date
            is_late = timezone.now() > assignment.due_date
            status_val = 'Late' if is_late else 'Submitted'

            if existing_sub:
                existing_sub.file_path = file_rel_path
                existing_sub.submitted_at = timezone.now()
                existing_sub.status = status_val
                existing_sub.save()
                messages.success(request, f"Assignment successfully resubmitted! (Status: {status_val})")
            else:
                Submission.objects.create(
                    assignment_id=assignment,
                    student_id=student,
                    file_path=file_rel_path,
                    submitted_at=timezone.now(),
                    status=status_val
                )
                messages.success(request, f"Assignment successfully submitted! (Status: {status_val})")

            return redirect('student_submissions')
    else:
        form = SubmissionUploadForm()

    context = {
        'assignment': assignment,
        'existing_sub': existing_sub,
        'form': form,
    }
    return render(request, 'student/submit.html', context)


@student_required
def student_submissions(request):
    """Manage own submissions: view, replace, or delete before deadline and evaluation."""
    student = request.user.student_profile
    submissions = Submission.objects.filter(student_id=student).select_related(
        'assignment_id', 'assignment_id__course_id', 'evaluation'
    ).order_by('-submitted_at')

    # Mark evaluated submissions as 'Returned' once viewed
    for s in submissions:
        if s.status == 'Evaluated':
            s.status = 'Returned'
            s.save(update_fields=['status'])

    return render(request, 'student/my_submissions.html', {'submissions': submissions})
=======
            uploaded_file = form.cleaned_data['submission_file']
            now = timezone.now()
            is_late = now > assignment.due_date
            status_val = 'Late' if is_late else 'Submitted'

            # Relative destination directory: media/submissions/<course>/<assignment>/
            course_id = assignment.course_id.course_id
            assign_id = assignment.assignment_id
            rel_dir = os.path.join('submissions', str(course_id), str(assign_id))
            full_dir = os.path.join(settings.MEDIA_ROOT, rel_dir)
            os.makedirs(full_dir, exist_ok=True)

            safe_name = f"{student.roll_no}_{uploaded_file.name}"
            dest_path = os.path.join(full_dir, safe_name)

            with open(dest_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)

            rel_file_path = f"{rel_dir}/{safe_name}".replace('\\', '/')

            if existing_sub:
                # Replace existing
                existing_sub.file_path = rel_file_path
                existing_sub.submitted_at = now
                existing_sub.status = status_val
                existing_sub.save()
                messages.success(request, f"Your assignment was successfully replaced! (Status: {status_val})")
                return redirect('student_submission_view', submission_id=existing_sub.submission_id)
            else:
                new_sub = Submission.objects.create(
                    assignment_id=assignment,
                    student_id=student,
                    file_path=rel_file_path,
                    submitted_at=now,
                    status=status_val
                )
                messages.success(request, f"Assignment submitted successfully! (Status: {status_val})")
                return redirect('student_submission_view', submission_id=new_sub.submission_id)
    else:
        form = SubmissionUploadForm()

    return render(request, 'student/submit.html', {
        'assignment': assignment,
        'form': form,
        'existing_sub': existing_sub,
        'is_past_due': timezone.now() > assignment.due_date,
    })


@student_required
def student_submission_view(request, submission_id):
    student = Student.objects.get(user=request.user)
    submission = get_object_or_404(Submission, submission_id=submission_id, student_id=student)
    evaluation = getattr(submission, 'evaluation', None)

    # When student views evaluated submission, update status to Returned
    if submission.status == 'Evaluated' and evaluation is not None:
        submission.status = 'Returned'
        submission.save()

    can_delete = (not submission.is_late) and (evaluation is None) and (timezone.now() <= submission.assignment_id.due_date)
    can_replace = (evaluation is None) and (timezone.now() <= submission.assignment_id.due_date)

    return render(request, 'student/submission_detail.html', {
        'submission': submission,
        'evaluation': evaluation,
        'can_delete': can_delete,
        'can_replace': can_replace,
    })
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


@student_required
def student_submission_delete(request, submission_id):
<<<<<<< HEAD
    """Delete own submission before deadline and before evaluation."""
    student = request.user.student_profile
    submission = get_object_or_404(Submission, submission_id=submission_id, student_id=student)

    # Check if evaluated
    if submission.status in ['Evaluated', 'Returned']:
        messages.error(request, "Cannot delete a submission that has already been evaluated.")
        return redirect('student_submissions')

    # Check if past due date
    if timezone.now() > submission.assignment_id.due_date:
        messages.error(request, "Cannot delete submission after the deadline.")
        return redirect('student_submissions')

    if request.method == 'POST':
        title = submission.assignment_id.title
        submission.delete()
        messages.success(request, f"Submission for '{title}' deleted successfully.")
        return redirect('student_submissions')

    return render(request, 'admin_panel/confirm_delete.html', {
        'item': submission,
        'type': 'Submission',
        'back_url': 'student_submissions'
=======
    student = Student.objects.get(user=request.user)
    submission = get_object_or_404(Submission, submission_id=submission_id, student_id=student)

    # Business rule: delete only before deadline and before evaluation
    if hasattr(submission, 'evaluation'):
        messages.error(request, "Cannot delete evaluated submission.")
        return redirect('student_submission_view', submission_id=submission.submission_id)
    if timezone.now() > submission.assignment_id.due_date:
        messages.error(request, "Deadline has passed. Deletion is not allowed.")
        return redirect('student_submission_view', submission_id=submission.submission_id)

    if request.method == 'POST':
        # Remove physical file if exists
        try:
            full_path = os.path.join(settings.MEDIA_ROOT, submission.file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception:
            pass
        submission.delete()
        messages.success(request, "Submission removed successfully. You may submit again before the deadline.")
        return redirect('student_assignments')

    return render(request, 'admin_panel/confirm_delete.html', {
        'object_name': f"Submission for {submission.assignment_id.title}",
        'item_type': 'Submission',
        'cancel_url': 'student_assignments'
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
    })


@student_required
<<<<<<< HEAD
def student_grades(request):
    """View grades, feedback and performance records."""
    student = request.user.student_profile
    submissions = Submission.objects.filter(
        student_id=student,
        status__in=['Evaluated', 'Returned']
    ).select_related('assignment_id', 'assignment_id__course_id', 'evaluation').order_by('-submitted_at')

    # Update status to Returned
    for s in submissions:
        if s.status == 'Evaluated':
            s.status = 'Returned'
            s.save(update_fields=['status'])

    return render(request, 'student/grades.html', {'submissions': submissions})


@student_required
def student_notifications(request):
    """Upcoming deadline reminders and grading alerts."""
    student = request.user.student_profile
    courses = Course.objects.filter(enrollments__student_id=student)
    assignments = Assignment.objects.filter(course_id__in=courses, due_date__gt=timezone.now()).order_by('due_date')
    recent_grades = Submission.objects.filter(student_id=student, status__in=['Evaluated', 'Returned']).order_by('-submitted_at')[:5]

    return render(request, 'student/notifications.html', {
        'upcoming_deadlines': assignments,
        'recent_grades': recent_grades,
    })


@student_required
def student_profile(request):
    """Student profile details."""
    student = request.user.student_profile
    return render(request, 'student/profile.html', {'student': student})


# ========================================================
# ERROR HANDLERS (403, 404, 500)
# ========================================================

def error_403(request, exception=None):
    return render(request, '403.html', {'message': '403 Forbidden: You do not have permission to access this resource.'}, status=403)


def error_404(request, exception=None):
    return render(request, '404.html', {'message': '404 Page Not Found: The requested resource could not be found.'}, status=404)


def error_500(request):
    return render(request, '500.html', {'message': '500 Internal Server Error: An unexpected error occurred on the server.'}, status=500)


def favicon(request):
    svg_icon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#1d4ed8"/><path d="M50 25 L80 42 L50 59 L20 42 Z" fill="#ffffff"/><path d="M35 52 L35 70 Q50 80 65 70 L65 52" fill="none" stroke="#ffffff" stroke-width="5"/></svg>'''
    return HttpResponse(svg_icon, content_type="image/svg+xml")

=======
def student_marks_feedback(request):
    student = Student.objects.get(user=request.user)
    evaluations = Evaluation.objects.filter(submission_id__student_id=student).select_related('submission_id__assignment_id', 'submission_id__assignment_id__course_id').order_by('-evaluated_on')
    
    total_marks_obtained = sum(e.marks for e in evaluations)
    total_possible_marks = sum(e.submission_id.assignment_id.max_marks for e in evaluations)
    overall_percentage = round((total_marks_obtained / total_possible_marks * 100), 1) if total_possible_marks > 0 else 0

    return render(request, 'student/marks_feedback.html', {
        'evaluations': evaluations,
        'total_marks_obtained': total_marks_obtained,
        'total_possible_marks': total_possible_marks,
        'overall_percentage': overall_percentage,
    })


# ==========================================
# SECURE FILE DOWNLOAD
# ==========================================

def download_file(request, file_type, item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if file_type == 'submission':
        submission = get_object_or_404(Submission, submission_id=item_id)
        # Check permissions: Admin, Teacher of course, or the Student who submitted
        is_admin = Admin.objects.filter(user=request.user).exists() or request.user.is_superuser
        is_teacher = Teacher.objects.filter(user=request.user, courses=submission.assignment_id.course_id).exists()
        is_student = Student.objects.filter(user=request.user, submissions=submission).exists()

        if not (is_admin or is_teacher or is_student):
            return HttpResponseForbidden("You do not have access to download this file.")

        full_path = os.path.join(settings.MEDIA_ROOT, submission.file_path)
        if not os.path.exists(full_path):
            raise Http404("File not found on server.")
        return FileResponse(open(full_path, 'rb'), as_attachment=True, filename=os.path.basename(full_path))

    elif file_type == 'assignment':
        assignment = get_object_or_404(Assignment, assignment_id=item_id)
        if not assignment.file_path:
            raise Http404("No attachment associated with this assignment.")
        full_path = os.path.join(settings.MEDIA_ROOT, assignment.file_path)
        if not os.path.exists(full_path):
            raise Http404("Attachment not found on server.")
        return FileResponse(open(full_path, 'rb'), as_attachment=True, filename=os.path.basename(full_path))

    raise Http404("Invalid file request.")
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
