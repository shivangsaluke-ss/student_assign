<<<<<<< HEAD
import os
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Admin, Teacher, Student, Course, Assignment, Submission, Evaluation


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control-cosmic',
            'placeholder': 'Enter your username or email',
            'autocomplete': 'off',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-cosmic',
            'placeholder': 'Enter your password',
            'autocomplete': 'new-password',
            'required': True
        })
    )
    role = forms.ChoiceField(
        choices=(('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')),
        required=False,
        widget=forms.HiddenInput()
    )


class StudentRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-cosmic',
            'placeholder': 'Confirm your password',
            'required': True
        })
    )

    class Meta:
        model = Student
        fields = ['student_name', 'student_email', 'roll_no', 'semester', 'student_password']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Full Name', 'required': True}),
            'student_email': forms.EmailInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Email Address', 'required': True}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'e.g. 3092 or 21010101', 'required': True}),
            'semester': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 1, 'max': 8, 'placeholder': 'Semester (1-8)', 'required': True}),
            'student_password': forms.PasswordInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Create Password', 'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('student_password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data


=======
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Admin, Teacher, Student, Course, Enrollment, Assignment, Submission, Evaluation
import os


class StudentRegisterForm(forms.Form):
    student_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Shivang Saluke'}))
    student_email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@gtu.edu.in'}))
    roll_no = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 23BCA3092'}))
    semester = forms.IntegerField(min_value=1, max_value=8, initial=5, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Choose strong password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password'}))

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', 'Passwords do not match.')

        email = cleaned_data.get('student_email')
        if email and (User.objects.filter(username=email).exists() or Student.objects.filter(student_email=email).exists()):
            self.add_error('student_email', 'An account with this email already exists.')

        roll = cleaned_data.get('roll_no')
        if roll and Student.objects.filter(roll_no=roll).exists():
            self.add_error('roll_no', 'This roll number is already registered.')

        return cleaned_data


class LoginForm(forms.Form):
    ROLE_CHOICES = (
        ('auto', 'Auto Detect Role'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter registered email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))


>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'teacher_id', 'semester']
        widgets = {
<<<<<<< HEAD
            'course_name': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Course Name', 'required': True}),
            'teacher_id': forms.Select(attrs={'class': 'form-control-cosmic', 'required': True}),
            'semester': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 1, 'max': 8, 'required': True}),
=======
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Advanced Java & Spring Boot'}),
            'teacher_id': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
        }


class TeacherForm(forms.ModelForm):
<<<<<<< HEAD
    class Meta:
        model = Teacher
        fields = ['teacher_name', 'teacher_email', 'department', 'teacher_password']
        widgets = {
            'teacher_name': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Teacher Full Name', 'required': True}),
            'teacher_email': forms.EmailInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Email Address', 'required': True}),
            'department': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Department (e.g. Computer Science)', 'required': True}),
            'teacher_password': forms.PasswordInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Password', 'required': True}),
=======
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep unchanged'}), help_text="Set or update login password")

    class Meta:
        model = Teacher
        fields = ['teacher_name', 'teacher_email', 'department']
        widgets = {
            'teacher_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dr. Priya Sharma'}),
            'teacher_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'priya.sharma@gtu.edu.in'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science & IT'}),
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
        }


class StudentAdminForm(forms.ModelForm):
<<<<<<< HEAD
    class Meta:
        model = Student
        fields = ['student_name', 'student_email', 'roll_no', 'semester', 'student_password']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Student Name', 'required': True}),
            'student_email': forms.EmailInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Email Address', 'required': True}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Roll No', 'required': True}),
            'semester': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 1, 'max': 8, 'required': True}),
            'student_password': forms.PasswordInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Password', 'required': True}),
=======
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep unchanged'}), help_text="Set or update login password")

    class Meta:
        model = Student
        fields = ['student_name', 'student_email', 'roll_no', 'semester']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student_id', 'course_id']
        widgets = {
            'student_id': forms.Select(attrs={'class': 'form-select'}),
            'course_id': forms.Select(attrs={'class': 'form-select'}),
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
        }


class AssignmentForm(forms.ModelForm):
<<<<<<< HEAD
    attachment = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-cosmic'}))
=======
    attachment = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course_id', 'due_date', 'max_marks']
        widgets = {
<<<<<<< HEAD
            'title': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Assignment Title', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control-cosmic', 'rows': 4, 'placeholder': 'Detailed instructions...', 'required': True}),
            'course_id': forms.Select(attrs={'class': 'form-control-cosmic', 'required': True}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control-cosmic', 'type': 'datetime-local', 'required': True}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 1, 'placeholder': 'Maximum Marks (e.g. 50)', 'required': True}),
        }

=======
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assignment title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed problem statement and guidelines...'}),
            'course_id': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
        }

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file:
            ext = os.path.splitext(file.name)[1].lower().replace('.', '')
            if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
                raise ValidationError(f"File extension '.{ext}' is not allowed. Supported: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}")
            if file.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError(f"File size exceeds 10 MB limit ({file.size / (1024*1024):.1f} MB uploaded).")
        return file

>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1

class SubmissionUploadForm(forms.Form):
    submission_file = forms.FileField(
        required=True,
<<<<<<< HEAD
        widget=forms.FileInput(attrs={'id': 'fileInput', 'class': 'd-none', 'accept': '.pdf,.doc,.docx,.zip,.jpg,.jpeg,.png'})
    )

    def clean_submission_file(self):
        f = self.cleaned_data.get('submission_file')
        if not f:
            raise ValidationError("No file uploaded.")
        # Validate file extension
        ext = os.path.splitext(f.name)[1].lower().lstrip('.')
        allowed = ['pdf', 'doc', 'docx', 'zip', 'jpg', 'jpeg', 'png']
        if ext not in allowed:
            raise ValidationError(f"Invalid file extension '.{ext}'. Allowed types: PDF, DOC, DOCX, ZIP, JPG, PNG.")
        # Validate size: max 10MB
        if f.size > 10 * 1024 * 1024:
            raise ValidationError("File size exceeds maximum allowed limit of 10 MB.")
        return f
=======
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'submissionFileInput'}),
        help_text="Allowed formats: PDF, DOC, DOCX, ZIP, JPG, PNG. Maximum file size: 10 MB."
    )

    def clean_submission_file(self):
        file = self.cleaned_data.get('submission_file')
        if file:
            ext = os.path.splitext(file.name)[1].lower().replace('.', '')
            if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
                raise ValidationError(f"Invalid file type '.{ext}'. Allowed types are: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}.")
            if file.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError(f"File size exceeds maximum limit of 10 MB. Current file size: {file.size / (1024*1024):.2f} MB.")
        return file
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['marks', 'feedback']
        widgets = {
<<<<<<< HEAD
            'marks': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 0, 'required': True}),
            'feedback': forms.Textarea(attrs={'class': 'form-control-cosmic', 'rows': 3, 'placeholder': 'Provide constructive feedback for the student...', 'required': True, 'maxlength': 250}),
=======
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Constructive review feedback for student...', 'maxlength': 250}),
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
        }

    def __init__(self, *args, max_marks=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_marks = max_marks
        self.fields['marks'].widget.attrs['max'] = max_marks
<<<<<<< HEAD
=======
        self.fields['marks'].help_text = f"Allowed range: 0 to {max_marks}"
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
<<<<<<< HEAD
            if marks < 0:
                raise ValidationError("Marks cannot be negative.")
            if marks > self.max_marks:
                raise ValidationError(f"Marks cannot exceed maximum marks ({self.max_marks}).")
        return marks
=======
            if marks < 0 or marks > self.max_marks:
                raise ValidationError(f"Marks must be between 0 and {self.max_marks}.")
        return marks


class AnnouncementForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), widget=forms.Select(attrs={'class': 'form-select'}))
    title = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write announcement to enrolled students...'}))

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher_id=teacher)
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
