from .models import Admin, Teacher, Student, Submission, Assignment, Enrollment, Evaluation, Course
from django.utils import timezone
from datetime import timedelta


def sams_context(request):
    context = {
        'user_role': None,
        'user_profile': None,
        'notifications': [],
        'unread_count': 0,
    }

    if not request.user.is_authenticated:
        return context

    # Check Admin
    try:
        admin_obj = Admin.objects.get(user=request.user)
        context['user_role'] = 'admin'
        context['user_profile'] = admin_obj
        # Admin notifications: pending evaluations
        pending_count = Submission.objects.filter(evaluation__isnull=True).count()
        if pending_count > 0:
            context['notifications'].append({
                'title': 'Submissions Pending Review',
                'message': f'{pending_count} submissions are awaiting evaluation across courses.',
                'link': '/admin-panel/submissions/?filter=pending',
                'type': 'info',
            })
        context['unread_count'] = len(context['notifications'])
        return context
    except Admin.DoesNotExist:
        pass

    # Check Teacher
    try:
        teacher_obj = Teacher.objects.get(user=request.user)
        context['user_role'] = 'teacher'
        context['user_profile'] = teacher_obj
        # Submissions pending review for teacher's courses
        pending_reviews = Submission.objects.filter(
            assignment_id__course_id__teacher_id=teacher_obj,
            evaluation__isnull=True
        ).count()
        if pending_reviews > 0:
            context['notifications'].append({
                'title': 'Submissions Ready for Grading',
                'message': f'You have {pending_reviews} pending submission(s) to evaluate.',
                'link': '/teacher/dashboard/',
                'type': 'warning',
            })
        context['unread_count'] = len(context['notifications'])
        return context
    except Teacher.DoesNotExist:
        pass

    # Check Student
    try:
        student_obj = Student.objects.get(user=request.user)
        context['user_role'] = 'student'
        context['user_profile'] = student_obj
        
        # 1. Recently evaluated submissions
        recent_evals = Evaluation.objects.filter(submission_id__student_id=student_obj).order_by('-evaluated_on')[:3]
        for ev in recent_evals:
            context['notifications'].append({
                'title': f'Result: {ev.submission_id.assignment_id.title}',
                'message': f'Marks: {ev.marks}/{ev.submission_id.assignment_id.max_marks} - {ev.feedback[:40]}...',
                'link': f'/student/submission/{ev.submission_id.submission_id}/',
                'type': 'success',
            })

        # 2. Upcoming deadlines in next 48 hours for enrolled courses without submission
        now = timezone.now()
        enrolled_courses = Course.objects.filter(enrollments__student_id=student_obj)
        submitted_assignment_ids = Submission.objects.filter(student_id=student_obj).values_list('assignment_id', flat=True)
        upcoming = Assignment.objects.filter(
            course_id__in=enrolled_courses,
            due_date__gt=now,
            due_date__lte=now + timedelta(days=2)
        ).exclude(assignment_id__in=submitted_assignment_ids)

        for up in upcoming:
            context['notifications'].append({
                'title': f'Deadline Alert: {up.title}',
                'message': f'Due on {up.due_date.strftime("%d %b, %I:%M %p")}',
                'link': f'/student/assignments/{up.assignment_id}/submit/',
                'type': 'danger',
            })

        context['unread_count'] = len(context['notifications'])
        return context
    except Student.DoesNotExist:
        pass

    if request.user.is_superuser:
        context['user_role'] = 'superuser'

    return context
