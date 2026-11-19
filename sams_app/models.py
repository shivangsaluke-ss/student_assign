from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


def assignment_upload_path(instance, filename):
    return f"assignments/{instance.course_id.course_id}/{filename}"


def submission_upload_path(instance, filename):
    course_id = instance.assignment_id.course_id.course_id
    assignment_id = instance.assignment_id.assignment_id
    return f"submissions/{course_id}/{assignment_id}/{filename}"


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=50)
    admin_email = models.CharField(max_length=50, unique=True)
    admin_password = models.CharField(max_length=100)
    admin_mobile = models.CharField(max_length=15, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile', null=True, blank=True)

    class Meta:
        db_table = 'admin'
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f"{self.admin_name} ({self.admin_email})"


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=50)
    teacher_email = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=50)
    teacher_password = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True)

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.teacher_name} - {self.department}"


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=50)
    student_email = models.CharField(max_length=50, unique=True)
    roll_no = models.CharField(max_length=15, unique=True)
    semester = models.IntegerField()
    student_password = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.student_name} ({self.roll_no}) - Sem {self.semester}"


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher_id', related_name='courses', db_index=True)
    semester = models.IntegerField()

    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.course_name} (Sem {self.semester})"


class Enrollment(models.Model):
    enroll_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id', related_name='enrollments', db_index=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_id', related_name='enrollments', db_index=True)
    enroll_date = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'enrollment'
        unique_together = (('student_id', 'course_id'),)
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f"{self.student_id.student_name} -> {self.course_id.course_name}"


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_id', related_name='assignments', db_index=True)
    due_date = models.DateTimeField(db_index=True)
    max_marks = models.IntegerField()
    file_path = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'assignment'
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.title} - {self.course_id.course_name}"

    @property
    def is_past_due(self):
        return timezone.now() > self.due_date

<<<<<<< HEAD
    @property
    def filename(self):
        return os.path.basename(self.file_path) if self.file_path else ''

=======
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1

class Submission(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Late', 'Late'),
        ('Evaluated', 'Evaluated'),
        ('Returned', 'Returned'),
    )

    submission_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE, db_column='assignment_id', related_name='submissions', db_index=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id', related_name='submissions', db_index=True)
    file_path = models.CharField(max_length=200)
    submitted_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='Submitted')

    class Meta:
        db_table = 'submission'
        unique_together = (('assignment_id', 'student_id'),)
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Submission by {self.student_id.student_name} on {self.assignment_id.title}"

    @property
    def filename(self):
        return os.path.basename(self.file_path) if self.file_path else ''

    @property
    def is_late(self):
        return self.submitted_at > self.assignment_id.due_date

    @property
    def status_badge_class(self):
        mapping = {
            'Pending': 'badge-pending',
            'Submitted': 'badge-submitted',
            'Late': 'badge-late',
            'Evaluated': 'badge-evaluated',
            'Returned': 'badge-returned',
        }
<<<<<<< HEAD
        return mapping.get(self.status, 'badge-submitted')
=======
        return mapping.get(self.status, 'badge-secondary')
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


class Evaluation(models.Model):
    evaluation_id = models.AutoField(primary_key=True)
    submission_id = models.OneToOneField(Submission, on_delete=models.CASCADE, db_column='submission_id', related_name='evaluation', unique=True, db_index=True)
    marks = models.IntegerField()
    feedback = models.CharField(max_length=250)
    evaluated_on = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'evaluation'
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'

    def __str__(self):
        return f"Evaluation for {self.submission_id}: {self.marks}/{self.submission_id.assignment_id.max_marks}"
