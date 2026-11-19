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


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'teacher_id', 'semester']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Course Name', 'required': True}),
            'teacher_id': forms.Select(attrs={'class': 'form-control-cosmic', 'required': True}),
            'semester': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 1, 'max': 8, 'required': True}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_name', 'teacher_email', 'department', 'teacher_password']
        widgets = {
            'teacher_name': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Teacher Full Name', 'required': True}),
            'teacher_email': forms.EmailInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Email Address', 'required': True}),
            'department': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Department (e.g. Computer Science)', 'required': True}),
            'teacher_password': forms.PasswordInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Password', 'required': True}),
        }


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_email', 'roll_no', 'semester', 'student_password']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Student Name', 'required': True}),
            'student_email': forms.EmailInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Email Address', 'required': True}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Roll No', 'required': True}),
            'semester': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 1, 'max': 8, 'required': True}),
            'student_password': forms.PasswordInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Password', 'required': True}),
        }


class AssignmentForm(forms.ModelForm):
    attachment = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-cosmic'}))

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course_id', 'due_date', 'max_marks']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control-cosmic', 'placeholder': 'Assignment Title', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control-cosmic', 'rows': 4, 'placeholder': 'Detailed instructions...', 'required': True}),
            'course_id': forms.Select(attrs={'class': 'form-control-cosmic', 'required': True}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control-cosmic', 'type': 'datetime-local', 'required': True}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 1, 'placeholder': 'Maximum Marks (e.g. 50)', 'required': True}),
        }


class SubmissionUploadForm(forms.Form):
    submission_file = forms.FileField(
        required=True,
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


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['marks', 'feedback']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control-cosmic', 'min': 0, 'required': True}),
            'feedback': forms.Textarea(attrs={'class': 'form-control-cosmic', 'rows': 3, 'placeholder': 'Provide constructive feedback for the student...', 'required': True, 'maxlength': 250}),
        }

    def __init__(self, *args, max_marks=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_marks = max_marks
        self.fields['marks'].widget.attrs['max'] = max_marks

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
            if marks < 0:
                raise ValidationError("Marks cannot be negative.")
            if marks > self.max_marks:
                raise ValidationError(f"Marks cannot exceed maximum marks ({self.max_marks}).")
        return marks
