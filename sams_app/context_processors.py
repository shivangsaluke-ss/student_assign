from django.utils import timezone
from .models import Admin, Teacher, Student, Assignment, Submission, Course, Enrollment

def sams_context(request):
    ctx = {
        'APP_NAME': 'Student Assignment Management System',
        'APP_SHORT': 'SAMS',
        'TAGLINE': 'Submit Smart. Grade Faster.',
        'user_role': None,
        'user_profile': None,
        'pending_reviews_count': 0,
        'upcoming_deadlines_count': 0,
    }

    if not request.user.is_authenticated:
        return ctx

    user = request.user
    if hasattr(user, 'admin_profile') or user.is_superuser:
        ctx['user_role'] = 'admin'
        try:
            ctx['user_profile'] = user.admin_profile
        except Exception:
            ctx['user_profile'] = None
    elif hasattr(user, 'teacher_profile'):
        ctx['user_role'] = 'teacher'
        teacher = user.teacher_profile
        ctx['user_profile'] = teacher
        # Count submissions awaiting grading
        teacher_courses = Course.objects.filter(teacher_id=teacher)
        ctx['pending_reviews_count'] = Submission.objects.filter(
            assignment_id__course_id__in=teacher_courses,
            status__in=['Submitted', 'Late']
        ).count()
    elif hasattr(user, 'student_profile'):
        ctx['user_role'] = 'student'
        student = user.student_profile
        ctx['user_profile'] = student
        # Upcoming assignments in enrolled courses
        enrolled_courses = Course.objects.filter(enrollments__student_id=student)
        submitted_assignment_ids = Submission.objects.filter(student_id=student).values_list('assignment_id', flat=True)
        ctx['upcoming_deadlines_count'] = Assignment.objects.filter(
            course_id__in=enrolled_courses,
            due_date__gt=timezone.now()
        ).exclude(assignment_id__in=submitted_assignment_ids).count()

    return ctx
