import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from sams_app.models import Admin, Teacher, Student, Course, Enrollment, Assignment, Submission, Evaluation

print("Seeding SAMS Demo Data...")

# 1. Admin
admin_email = 'admin@sams.gtu.ac.in'
admin_user, _ = User.objects.get_or_create(username=admin_email, defaults={'email': admin_email, 'first_name': 'System', 'last_name': 'Admin'})
admin_user.set_password('admin123')
admin_user.is_superuser = True
admin_user.is_staff = True
admin_user.save()

admin_profile, _ = Admin.objects.get_or_create(
    admin_email=admin_email,
    defaults={
        'admin_name': 'System Administrator',
        'admin_password': 'hash_admin123',
        'admin_mobile': '9876543210',
        'user': admin_user
    }
)
admin_profile.user = admin_user
admin_profile.save()
print("Created Admin:", admin_email)

# 2. Teacher
teacher_email = 'priya.sharma@gtu.ac.in'
teacher_user, _ = User.objects.get_or_create(username=teacher_email, defaults={'email': teacher_email, 'first_name': 'Dr. Priya', 'last_name': 'Sharma'})
teacher_user.set_password('teacher123')
teacher_user.save()

teacher_profile, _ = Teacher.objects.get_or_create(
    teacher_email=teacher_email,
    defaults={
        'teacher_name': 'Dr. Priya Sharma',
        'department': 'Computer Applications (BCA)',
        'teacher_password': 'hash_teacher123',
        'user': teacher_user
    }
)
teacher_profile.user = teacher_user
teacher_profile.save()
print("Created Teacher:", teacher_email)

# 3. Student
student_email = 'shivang@student.gtu.ac.in'
student_user, _ = User.objects.get_or_create(username=student_email, defaults={'email': student_email, 'first_name': 'Saluke', 'last_name': 'Shivang'})
student_user.set_password('student123')
student_user.save()

student_profile, _ = Student.objects.get_or_create(
    student_email=student_email,
    defaults={
        'student_name': 'Saluke Shivang',
        'roll_no': '210200107001',
        'semester': 5,
        'student_password': 'hash_student123',
        'user': student_user
    }
)
student_profile.user = student_user
student_profile.save()
print("Created Student:", student_email)

# 4. Courses
course1, _ = Course.objects.get_or_create(
    course_name='Web Programming & Frameworks',
    semester=5,
    defaults={'teacher_id': teacher_profile}
)

course2, _ = Course.objects.get_or_create(
    course_name='Software Engineering & Agile Methodologies',
    semester=5,
    defaults={'teacher_id': teacher_profile}
)

course3, _ = Course.objects.get_or_create(
    course_name='Cloud Computing & Microservices',
    semester=5,
    defaults={'teacher_id': teacher_profile}
)
print("Created Courses.")

# 5. Enrollments
for c in [course1, course2, course3]:
    Enrollment.objects.get_or_create(student_id=student_profile, course_id=c)
print("Enrolled Student into Courses.")

# 6. Assignments
now = timezone.now()

# Assignment 1: Past Due & Evaluated
a1, _ = Assignment.objects.get_or_create(
    title='Lab 1: Django MTV Architecture & Authentication',
    course_id=course1,
    defaults={
        'description': 'Implement user authentication, registration, and role-based redirect using Django session auth and custom decorators.',
        'due_date': now - timedelta(days=5),
        'max_marks': 25
    }
)

# Assignment 2: Due Soon (Impending)
a2, _ = Assignment.objects.get_or_create(
    title='Lab 2: RESTful API Integration & JSON Endpoints',
    course_id=course1,
    defaults={
        'description': 'Build clean RESTful endpoints for submission retrieval and evaluate performance with unit tests.',
        'due_date': now + timedelta(days=1, hours=8),
        'max_marks': 30
    }
)

# Assignment 3: Software Engineering Case Study
a3, _ = Assignment.objects.get_or_create(
    title='Case Study: Agile Sprint Planning & Jira Workflows',
    course_id=course2,
    defaults={
        'description': 'Prepare a comprehensive sprint backlog and release documentation for an academic portal project.',
        'due_date': now + timedelta(days=6),
        'max_marks': 20
    }
)
print("Created Assignments.")

# 7. Submissions & Evaluations
# Make sure media dir exists
os.makedirs('media/submissions', exist_ok=True)

# Fake submission file for a1
sub1, _ = Submission.objects.get_or_create(
    assignment_id=a1,
    student_id=student_profile,
    defaults={
        'file_path': 'submissions/1/1/210200107001_lab1_submission.pdf',
        'submitted_at': now - timedelta(days=6),
        'status': 'Evaluated'
    }
)

# Evaluation for sub1
Evaluation.objects.get_or_create(
    submission_id=sub1,
    defaults={
        'marks': 23,
        'feedback': 'Excellent implementation! Clean code structure and robust security checks.',
        'evaluated_on': (now - timedelta(days=4)).date()
    }
)
print("Created sample Submission and Evaluation.")
print("Database Seeding Completed Successfully!")

