import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Q
from django.conf import settings
from django.http import HttpResponse, Http404

from .models import Admin, Teacher, Student, Course, Enrollment, Assignment, Submission, Evaluation
from .forms import (
    LoginForm, StudentRegistrationForm, CourseForm, TeacherForm,
    StudentAdminForm, AssignmentForm, SubmissionUploadForm, EvaluationForm
)
from .decorators import admin_required, teacher_required, student_required


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
    return render(request, 'public/modules.html')


def diagrams(request):
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
        if form.is_valid():
            name = form.cleaned_data['student_name']
            email = form.cleaned_data['student_email']
            roll = form.cleaned_data['roll_no']
            sem = form.cleaned_data['semester']
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

            login(request, user)
            messages.success(request, f"Registration successful! Welcome to SAMS, {name}.")
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'public/register.html', {'form': form})


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


@admin_required
def admin_courses(request):
    """Manage courses list."""
    courses = Course.objects.select_related('teacher_id').annotate(
        students_count=Count('enrollments', distinct=True),
        assignments_count=Count('assignments', distinct=True)
    ).order_by('semester', 'course_name')
    teachers = Teacher.objects.all()
    return render(request, 'admin_panel/courses.html', {'courses': courses, 'teachers': teachers})


@admin_required
def admin_course_add(request):
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


@admin_required
def admin_course_edit(request, course_id):
    """Edit an existing course."""
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.course_name}' updated.")
            return redirect('admin_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin_panel/course_form.html', {'form': form, 'course': course, 'title': 'Edit Course'})


@admin_required
def admin_course_delete(request, course_id):
    """Delete a course."""
    course = get_object_or_404(Course, course_id=course_id)
    if request.method == 'POST':
        name = course.course_name
        course.delete()
        messages.success(request, f"Course '{name}' has been deleted.")
        return redirect('admin_courses')
    return render(request, 'admin_panel/confirm_delete.html', {'item': course, 'type': 'Course', 'back_url': 'admin_courses'})


@admin_required
def admin_teachers(request):
    """Manage teachers list."""
    teachers = Teacher.objects.annotate(courses_count=Count('courses')).order_by('teacher_name')
    return render(request, 'admin_panel/teachers.html', {'teachers': teachers})


@admin_required
def admin_teacher_add(request):
    """Register a new teacher."""
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['teacher_email']
            name = form.cleaned_data['teacher_name']
            dept = form.cleaned_data['department']
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


@admin_required
def admin_teacher_edit(request, teacher_id):
    """Edit teacher details."""
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
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


@admin_required
def admin_teacher_delete(request, teacher_id):
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


@admin_required
def admin_students(request):
    """Manage students list."""
    students = Student.objects.annotate(
        enrollments_count=Count('enrollments', distinct=True),
        submissions_count=Count('submissions', distinct=True)
    ).order_by('semester', 'roll_no')
    return render(request, 'admin_panel/students.html', {'students': students})


@admin_required
def admin_student_add(request):
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
    else:
        form = StudentAdminForm()
    return render(request, 'admin_panel/student_form.html', {'form': form, 'title': 'Add Student'})


@admin_required
def admin_student_edit(request, student_id):
    """Edit student profile."""
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        form = StudentAdminForm(request.POST, instance=student)
        if form.is_valid():
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


@admin_required
def admin_student_delete(request, student_id):
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


@admin_required
def admin_assignments(request):
    """Monitor all assignments and overall submissions across the portal."""
    assignments = Assignment.objects.select_related('course_id', 'course_id__teacher_id').annotate(
        total_subs=Count('submissions', distinct=True)
    ).order_by('-due_date')
    return render(request, 'admin_panel/assignments.html', {'assignments': assignments})


@admin_required
def admin_reports(request):
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


@admin_required
def admin_profile(request):
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


@teacher_required
def teacher_assignments(request):
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


@teacher_required
def teacher_assignment_edit(request, assignment_id):
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


@teacher_required
def teacher_assignment_delete(request, assignment_id):
    """Delete an assignment."""
    teacher = request.user.teacher_profile
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id, course_id__teacher_id=teacher)
    if request.method == 'POST':
        title = assignment.title
        assignment.delete()
        messages.success(request, f"Assignment '{title}' deleted.")
        return redirect('teacher_assignments')
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


@teacher_required
def teacher_announcements(request):
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


@student_required
def student_courses(request):
    """View enrolled courses and assigned teachers."""
    student = request.user.student_profile
    enrollments = Enrollment.objects.filter(student_id=student).select_related('course_id', 'course_id__teacher_id')
    return render(request, 'student/courses.html', {'enrollments': enrollments})


@student_required
def student_assignments(request):
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
        })

    return render(request, 'student/assignments.html', {'assignment_data': assignment_data})


@student_required
def student_submit(request, assignment_id):
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

    if request.method == 'POST':
        form = SubmissionUploadForm(request.POST, request.FILES)
        if form.is_valid():
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


@student_required
def student_submission_delete(request, submission_id):
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
    })


@student_required
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

