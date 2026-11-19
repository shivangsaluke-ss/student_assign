<<<<<<< HEAD
import os
from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from sams_app.models import Admin, Teacher, Student, Course, Enrollment, Assignment, Submission, Evaluation


class SAMSTests(TestCase):
    def setUp(self):
        self.client = Client()

        # 1. Create Admin
        self.admin_user = User.objects.create_user(username='test_admin', email='admin@test.com', password='password123')
        self.admin = Admin.objects.create(
            admin_name='Test Admin',
            admin_email='admin@test.com',
            admin_password=self.admin_user.password,
            admin_mobile='9999999999',
            user=self.admin_user
        )

        # 2. Create Teacher
        self.teacher_user = User.objects.create_user(username='test_teacher', email='teacher@test.com', password='password123')
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            teacher_email='teacher@test.com',
            department='Computer Science',
            teacher_password=self.teacher_user.password,
            user=self.teacher_user
        )

        # 3. Create Course
        self.course = Course.objects.create(
            course_name='Test Python & Django',
            teacher_id=self.teacher,
            semester=5
        )

        # 4. Create Student
        self.student_user = User.objects.create_user(username='test_student', email='student@test.com', password='password123')
        self.student = Student.objects.create(
            student_name='Test Student',
            student_email='student@test.com',
            roll_no='9999',
            semester=5,
            student_password=self.student_user.password,
            user=self.student_user
        )
        self.enrollment = Enrollment.objects.create(student_id=self.student, course_id=self.course)

        # 5. Create Active Assignment & Past Due Assignment
        self.assignment = Assignment.objects.create(
            title='Assignment Active',
            description='Active task instructions',
            course_id=self.course,
            due_date=timezone.now() + timedelta(days=2),
            max_marks=50
        )
        self.past_assignment = Assignment.objects.create(
            title='Assignment Past Due',
            description='Past due task',
            course_id=self.course,
            due_date=timezone.now() - timedelta(days=1),
            max_marks=50
        )

    def test_public_pages_render(self):
        """All public pages must return 200 OK with correct status."""
        routes = ['/', '/about/', '/modules/', '/diagrams/', '/database/', '/team/', '/login/', '/register/']
        for r in routes:
            resp = self.client.get(r)
            self.assertEqual(resp.status_code, 200, f"Route {r} failed with status {resp.status_code}")

    def test_role_based_access_control_403(self):
        """Users accessing wrong-role pages must receive HTTP 403 Forbidden."""
        # Student trying to access admin panel -> 403
        self.client.login(username='test_student', password='password123')
        resp = self.client.get('/admin-panel/')
        self.assertEqual(resp.status_code, 403)

        # Student trying to access teacher panel -> 403
        resp = self.client.get('/teacher/')
        self.assertEqual(resp.status_code, 403)
        self.client.logout()

        # Teacher trying to access admin panel -> 403
        self.client.login(username='test_teacher', password='password123')
        resp = self.client.get('/admin-panel/')
        self.assertEqual(resp.status_code, 403)

        # Teacher trying to access student portal -> 403
        resp = self.client.get('/student/')
        self.assertEqual(resp.status_code, 403)
        self.client.logout()

        # Admin trying to access student portal -> 403
        self.client.login(username='test_admin', password='password123')
        resp = self.client.get('/student/')
        self.assertEqual(resp.status_code, 403)

    def test_submission_evaluation_lifecycle_flow(self):
        """Full lifecycle: student submits -> late status check -> teacher grades -> student views -> Returned."""
        self.client.login(username='test_student', password='password123')

        # 1. Student submits active assignment (On time)
        test_file = SimpleUploadedFile("solution.pdf", b"%PDF-1.4 sample content", content_type="application/pdf")
        resp = self.client.post(f'/student/submit/{self.assignment.assignment_id}/', {'submission_file': test_file}, follow=True)
        self.assertEqual(resp.status_code, 200)

        sub = Submission.objects.get(assignment_id=self.assignment, student_id=self.student)
        self.assertEqual(sub.status, 'Submitted')
        self.assertFalse(sub.is_late)

        # 2. Student submits past due assignment (Late)
        late_file = SimpleUploadedFile("late_solution.pdf", b"%PDF-1.4 late content", content_type="application/pdf")
        self.client.post(f'/student/submit/{self.past_assignment.assignment_id}/', {'submission_file': late_file}, follow=True)
        late_sub = Submission.objects.get(assignment_id=self.past_assignment, student_id=self.student)
        self.assertEqual(late_sub.status, 'Late')
        self.assertTrue(late_sub.is_late)

        self.client.logout()

        # 3. Teacher evaluates student submission
        self.client.login(username='test_teacher', password='password123')
        eval_resp = self.client.post(f'/teacher/evaluate/{sub.submission_id}/', {
            'marks': 45,
            'feedback': 'Great implementation and design!'
        }, follow=True)
        self.assertEqual(eval_resp.status_code, 200)

        sub.refresh_from_db()
        self.assertEqual(sub.status, 'Evaluated')
        self.assertTrue(hasattr(sub, 'evaluation'))
        self.assertEqual(sub.evaluation.marks, 45)

        self.client.logout()

        # 4. Student views grades -> Status transitions to 'Returned'
        self.client.login(username='test_student', password='password123')
        grades_resp = self.client.get('/student/grades/')
        self.assertEqual(grades_resp.status_code, 200)

        sub.refresh_from_db()
        self.assertEqual(sub.status, 'Returned')
=======
from django.test import TestCase

# Create your tests here.
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
