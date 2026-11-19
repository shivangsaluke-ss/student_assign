import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from sams_app.models import Admin, Teacher, Student, Course, Enrollment, Assignment, Submission, Evaluation


class Command(BaseCommand):
    help = 'Seeds database with BCA Semester 5 SAMS demo data (Admin, Teachers, Students, Courses, Assignments, Submissions, Evaluations)'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding for SAMS...")

        # 1. Clear existing data safely
        Evaluation.objects.all().delete()
        Submission.objects.all().delete()
        Assignment.objects.all().delete()
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        Admin.objects.all().delete()
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # 2. Seed 1 Admin
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@gtu.ac.in', 'first_name': 'Prof. R. K. Patel', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('admin123')
        admin_user.save()

        Admin.objects.create(
            admin_name='Prof. R. K. Patel',
            admin_email='admin@gtu.ac.in',
            admin_password=admin_user.password,
            admin_mobile='9825012345',
            user=admin_user
        )
        self.stdout.write(self.style.SUCCESS("✓ Admin created: admin / admin123"))

        # 3. Seed 3 Teachers
        teachers_data = [
            ('Dr. Anita Sharma', 'anita.sharma@gtu.ac.in', 'Computer Science', 'teacher_anita'),
            ('Prof. Vikram Mehta', 'vikram.mehta@gtu.ac.in', 'Information Technology', 'teacher_vikram'),
            ('Prof. Neha Patel', 'neha.patel@gtu.ac.in', 'Software Engineering', 'teacher_neha'),
        ]

        teacher_objs = []
        for name, email, dept, username in teachers_data:
            u, _ = User.objects.get_or_create(username=username, defaults={'email': email, 'first_name': name})
            u.set_password('teacher123')
            u.save()

            t = Teacher.objects.create(
                teacher_name=name,
                teacher_email=email,
                department=dept,
                teacher_password=u.password,
                user=u
            )
            teacher_objs.append(t)
        self.stdout.write(self.style.SUCCESS("✓ 3 Teachers created (password: teacher123)"))

        # 4. Seed 4 Courses
        courses_data = [
            ('Web Development with Django & Python', teacher_objs[0], 5),
            ('Database Management Systems & MySQL', teacher_objs[1], 5),
            ('System Analysis & Design Methods', teacher_objs[2], 5),
            ('Object-Oriented Software Engineering', teacher_objs[0], 5),
        ]

        course_objs = []
        for cname, t_obj, sem in courses_data:
            c = Course.objects.create(course_name=cname, teacher_id=t_obj, semester=sem)
            course_objs.append(c)
        self.stdout.write(self.style.SUCCESS("✓ 4 Courses created"))

        # 5. Seed 12 Students
        students_data = [
            ('Dishant Jain', 'dishant@student.gtu.ac.in', '3031', 5),
            ('Mehul Jain', 'mehul@student.gtu.ac.in', '3032', 5),
            ('Shivang Saluke', 'shivang@student.gtu.ac.in', '3092', 5),
            ('Aarav Sharma', 'aarav@student.gtu.ac.in', '3041', 5),
            ('Diya Patel', 'diya@student.gtu.ac.in', '3042', 5),
            ('Rohan Shah', 'rohan@student.gtu.ac.in', '3043', 5),
            ('Priya Desai', 'priya@student.gtu.ac.in', '3044', 5),
            ('Kabir Joshi', 'kabir@student.gtu.ac.in', '3045', 5),
            ('Ananya Mehta', 'ananya@student.gtu.ac.in', '3046', 5),
            ('Yash Varma', 'yash@student.gtu.ac.in', '3047', 5),
            ('Sneha Trivedi', 'sneha@student.gtu.ac.in', '3048', 5),
            ('Dev Kothari', 'dev@student.gtu.ac.in', '3049', 5),
        ]

        student_objs = []
        for name, email, roll, sem in students_data:
            username = f"std_{roll}"
            u, _ = User.objects.get_or_create(username=username, defaults={'email': email, 'first_name': name})
            u.set_password('student123')
            u.save()

            s = Student.objects.create(
                student_name=name,
                student_email=email,
                roll_no=roll,
                semester=sem,
                student_password=u.password,
                user=u
            )
            student_objs.append(s)

            # Enroll each student into all 4 semester 5 courses
            for c in course_objs:
                Enrollment.objects.create(student_id=s, course_id=c, enroll_date=timezone.now().date())

        self.stdout.write(self.style.SUCCESS("✓ 12 Students created and enrolled (password: student123)"))

        # 6. Seed 6 Assignments (mix of past due and upcoming)
        now = timezone.now()
        assignments_data = [
            (
                "Assignment 1: Django Architecture & MVT Setup",
                "Implement a modular Django 5 web application with custom models, migrations, and template inheritance using CSS design tokens.",
                course_objs[0],
                now - timedelta(days=5), # Past due
                50
            ),
            (
                "Assignment 2: MySQL Database Normalization & ER Modeling",
                "Design a 3NF normalized schema for Student Assignment Management. Include foreign key constraints and indexing for submission status.",
                course_objs[1],
                now - timedelta(days=2), # Past due
                50
            ),
            (
                "Assignment 3: System Flow & UML Sequence Diagrams",
                "Draw complete UML diagrams (System Flow, Use Case, Sequence, Class) as per SAD project guidelines in Draw.io or VS Code.",
                course_objs[2],
                now - timedelta(days=1), # Past due
                40
            ),
            (
                "Assignment 4: Role-Based Access Control & CSRF Protection",
                "Implement secure authentication with decorators (@admin_required, @teacher_required, @student_required) and strict CSRF tokens.",
                course_objs[3],
                now + timedelta(days=3), # Upcoming
                50
            ),
            (
                "Assignment 5: Web Animations API & Responsive Layout",
                "Restyle user interface components using CSS custom properties (--color-*, --radius-*) and handle viewport sizes <= 820px.",
                course_objs[0],
                now + timedelta(days=7), # Upcoming
                50
            ),
            (
                "Assignment 6: BCA Semester 5 Capstone Submission",
                "Submit the complete project report, code repository documentation, and user manual for GTU final internal evaluation.",
                course_objs[2],
                now + timedelta(days=14), # Upcoming
                100
            ),
        ]

        assignment_objs = []
        for title, desc, course, due, marks in assignments_data:
            a = Assignment.objects.create(
                title=title,
                description=desc,
                course_id=course,
                due_date=due,
                max_marks=marks
            )
            assignment_objs.append(a)
        self.stdout.write(self.style.SUCCESS("✓ 6 Assignments created"))

        # 7. Seed Submissions & Evaluations (mix of Evaluated, Returned, Submitted, Late)
        # Helper to create sample file on disk
        def make_sample_file(course_id, assignment_id, roll_no):
            rel_dir = os.path.join('submissions', str(course_id), str(assignment_id))
            abs_dir = os.path.join(settings.MEDIA_ROOT, rel_dir)
            os.makedirs(abs_dir, exist_ok=True)
            fname = f"{roll_no}_assignment_solution.pdf"
            abs_path = os.path.join(abs_dir, fname)
            if not os.path.exists(abs_path):
                with open(abs_path, 'w', encoding='utf-8') as f:
                    f.write(f"%PDF-1.4 SAMS Demo Submission\nStudent Roll No: {roll_no}\nCourse: {course_id}\nAssignment: {assignment_id}\nSubmitted via SAMS Portal.")
            return os.path.join(rel_dir, fname)

        # Assignment 1 (Past due - 5 days ago)
        # Dishant: Submitted on time, Evaluated (48/50)
        f1 = make_sample_file(course_objs[0].course_id, assignment_objs[0].assignment_id, '3031')
        sub1 = Submission.objects.create(
            assignment_id=assignment_objs[0],
            student_id=student_objs[0],
            file_path=f1,
            submitted_at=assignment_objs[0].due_date - timedelta(hours=12),
            status='Returned'
        )
        Evaluation.objects.create(
            submission_id=sub1,
            marks=48,
            feedback="Excellent MVT architecture! Clear separation of concerns and robust template filters.",
            evaluated_on=(now - timedelta(days=3)).date()
        )

        # Mehul: Submitted on time, Evaluated (46/50)
        f2 = make_sample_file(course_objs[0].course_id, assignment_objs[0].assignment_id, '3032')
        sub2 = Submission.objects.create(
            assignment_id=assignment_objs[0],
            student_id=student_objs[1],
            file_path=f2,
            submitted_at=assignment_objs[0].due_date - timedelta(hours=6),
            status='Evaluated'
        )
        Evaluation.objects.create(
            submission_id=sub2,
            marks=46,
            feedback="Well documented views and decorators. Design tokens match specification nicely.",
            evaluated_on=(now - timedelta(days=3)).date()
        )

        # Shivang: Late submission, Evaluated (44/50)
        f3 = make_sample_file(course_objs[0].course_id, assignment_objs[0].assignment_id, '3092')
        sub3 = Submission.objects.create(
            assignment_id=assignment_objs[0],
            student_id=student_objs[2],
            file_path=f3,
            submitted_at=assignment_objs[0].due_date + timedelta(hours=8), # Late!
            status='Evaluated'
        )
        Evaluation.objects.create(
            submission_id=sub3,
            marks=44,
            feedback="Good implementation of token-based CSS. Slight penalty for 8h late submission.",
            evaluated_on=(now - timedelta(days=2)).date()
        )

        # Aarav: Submitted on time, Awaiting Evaluation
        f4 = make_sample_file(course_objs[0].course_id, assignment_objs[0].assignment_id, '3041')
        Submission.objects.create(
            assignment_id=assignment_objs[0],
            student_id=student_objs[3],
            file_path=f4,
            submitted_at=assignment_objs[0].due_date - timedelta(hours=4),
            status='Submitted'
        )

        # Assignment 2 (Past due - 2 days ago)
        # Dishant: Submitted on time, Evaluated (49/50)
        f5 = make_sample_file(course_objs[1].course_id, assignment_objs[1].assignment_id, '3031')
        sub5 = Submission.objects.create(
            assignment_id=assignment_objs[1],
            student_id=student_objs[0],
            file_path=f5,
            submitted_at=assignment_objs[1].due_date - timedelta(hours=14),
            status='Returned'
        )
        Evaluation.objects.create(
            submission_id=sub5,
            marks=49,
            feedback="Outstanding ER design and indexing strategy. Exact match with GTU guidelines.",
            evaluated_on=(now - timedelta(days=1)).date()
        )

        # Mehul: Late submission, Awaiting evaluation
        f6 = make_sample_file(course_objs[1].course_id, assignment_objs[1].assignment_id, '3032')
        Submission.objects.create(
            assignment_id=assignment_objs[1],
            student_id=student_objs[1],
            file_path=f6,
            submitted_at=assignment_objs[1].due_date + timedelta(hours=5), # Late!
            status='Late'
        )

        # Shivang: Submitted on time, Awaiting evaluation
        f7 = make_sample_file(course_objs[1].course_id, assignment_objs[1].assignment_id, '3092')
        Submission.objects.create(
            assignment_id=assignment_objs[1],
            student_id=student_objs[2],
            file_path=f7,
            submitted_at=assignment_objs[1].due_date - timedelta(hours=2),
            status='Submitted'
        )

        # Assignment 3 (Past due - 1 day ago)
        # Dishant: Late submission, Awaiting evaluation
        f8 = make_sample_file(course_objs[2].course_id, assignment_objs[2].assignment_id, '3031')
        Submission.objects.create(
            assignment_id=assignment_objs[2],
            student_id=student_objs[0],
            file_path=f8,
            submitted_at=assignment_objs[2].due_date + timedelta(hours=3),
            status='Late'
        )

        # Shivang: Submitted on time, Evaluated (38/40)
        f9 = make_sample_file(course_objs[2].course_id, assignment_objs[2].assignment_id, '3092')
        sub9 = Submission.objects.create(
            assignment_id=assignment_objs[2],
            student_id=student_objs[2],
            file_path=f9,
            submitted_at=assignment_objs[2].due_date - timedelta(hours=10),
            status='Returned'
        )
        Evaluation.objects.create(
            submission_id=sub9,
            marks=38,
            feedback="Clean UML diagrams with clear actor boundaries and sequence activation boxes.",
            evaluated_on=now.date()
        )

        # Assignment 4 (Upcoming in 3 days)
        # Diya Patel: Submitted early!
        f10 = make_sample_file(course_objs[3].course_id, assignment_objs[3].assignment_id, '3042')
        Submission.objects.create(
            assignment_id=assignment_objs[3],
            student_id=student_objs[4],
            file_path=f10,
            submitted_at=now - timedelta(hours=3),
            status='Submitted'
        )

        self.stdout.write(self.style.SUCCESS("✓ Submissions and Evaluations seeded with Submitted, Late, Evaluated, and Returned lifecycle states!"))
        self.stdout.write(self.style.SUCCESS("Demo credentials summary:"))
        self.stdout.write("  Admin:   admin / admin123")
        self.stdout.write("  Teacher: anita.sharma@gtu.ac.in (or teacher_anita) / teacher123")
        self.stdout.write("  Student: std_3092 (or shivang@student.gtu.ac.in) / student123")
        self.stdout.write("  Student: std_3031 (or dishant@student.gtu.ac.in) / student123")
        self.stdout.write("  Student: std_3032 (or mehul@student.gtu.ac.in) / student123")
