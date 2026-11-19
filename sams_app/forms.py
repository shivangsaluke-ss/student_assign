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


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'teacher_id', 'semester']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Advanced Java & Spring Boot'}),
            'teacher_id': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
        }


class TeacherForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep unchanged'}), help_text="Set or update login password")

    class Meta:
        model = Teacher
        fields = ['teacher_name', 'teacher_email', 'department']
        widgets = {
            'teacher_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dr. Priya Sharma'}),
            'teacher_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'priya.sharma@gtu.edu.in'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science & IT'}),
        }


class StudentAdminForm(forms.ModelForm):
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
        }


class AssignmentForm(forms.ModelForm):
    attachment = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course_id', 'due_date', 'max_marks']
        widgets = {
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


class SubmissionUploadForm(forms.Form):
    submission_file = forms.FileField(
        required=True,
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


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['marks', 'feedback']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Constructive review feedback for student...', 'maxlength': 250}),
        }

    def __init__(self, *args, max_marks=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_marks = max_marks
        self.fields['marks'].widget.attrs['max'] = max_marks
        self.fields['marks'].help_text = f"Allowed range: 0 to {max_marks}"

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
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
