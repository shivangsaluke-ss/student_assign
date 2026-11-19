from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('modules/', views.modules_page, name='modules'),
    path('diagrams/', views.diagrams, name='diagrams'),
    path('database/', views.database_schema, name='database'),
    path('team/', views.team, name='team'),

    # Auth
    path('login/', views.user_login, name='login'),
    path('student/login/', views.student_login, name='student_login'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_student, name='register'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path('switch-role/<str:role>/', views.switch_role, name='switch_role'),

    # Admin Panel
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/courses/', views.admin_courses, name='admin_courses'),
    path('admin-panel/courses/add/', views.admin_course_add, name='admin_course_add'),
    path('admin-panel/courses/<int:course_id>/edit/', views.admin_course_edit, name='admin_course_edit'),
    path('admin-panel/courses/<int:course_id>/delete/', views.admin_course_delete, name='admin_course_delete'),
    path('admin-panel/teachers/', views.admin_teachers, name='admin_teachers'),
    path('admin-panel/teachers/add/', views.admin_teacher_add, name='admin_teacher_add'),
    path('admin-panel/teachers/<int:teacher_id>/edit/', views.admin_teacher_edit, name='admin_teacher_edit'),
    path('admin-panel/teachers/<int:teacher_id>/delete/', views.admin_teacher_delete, name='admin_teacher_delete'),
    path('admin-panel/students/', views.admin_students, name='admin_students'),
    path('admin-panel/students/add/', views.admin_student_add, name='admin_student_add'),
    path('admin-panel/students/<int:student_id>/edit/', views.admin_student_edit, name='admin_student_edit'),
    path('admin-panel/students/<int:student_id>/delete/', views.admin_student_delete, name='admin_student_delete'),
    path('admin-panel/enrollments/', views.admin_enrollments, name='admin_enrollments'),
    path('admin-panel/enrollments/<int:enroll_id>/delete/', views.admin_enrollment_delete, name='admin_enrollment_delete'),
    path('admin-panel/assignments/', views.admin_assignments, name='admin_assignments'),
    path('admin-panel/submissions/', views.admin_submissions, name='admin_submissions'),
    path('admin-panel/reports/', views.admin_reports, name='admin_reports'),
    path('admin-panel/profile/', views.admin_profile, name='admin_profile'),

    # Teacher Portal
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/courses/', views.teacher_courses, name='teacher_courses'),
    path('teacher/assignments/', views.teacher_assignments, name='teacher_assignments'),
    path('teacher/assignments/add/', views.teacher_assignment_add, name='teacher_assignment_add'),
    path('teacher/assignments/<int:assignment_id>/edit/', views.teacher_assignment_edit, name='teacher_assignment_edit'),
    path('teacher/assignments/<int:assignment_id>/delete/', views.teacher_assignment_delete, name='teacher_assignment_delete'),
    path('teacher/assignments/<int:assignment_id>/submissions/', views.teacher_assignment_submissions, name='teacher_assignment_submissions'),
    path('teacher/submissions/', views.teacher_submissions, name='teacher_submissions'),
    path('teacher/submissions/<int:submission_id>/grade/', views.teacher_grade_submission, name='teacher_grade_submission'),
    path('teacher/students/', views.teacher_students, name='teacher_students'),
    path('teacher/announcements/', views.teacher_announcements, name='teacher_announcements'),

    # Student Portal
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/courses/', views.student_courses, name='student_courses'),
    path('student/assignments/', views.student_assignments, name='student_assignments'),
    path('student/assignments/<int:assignment_id>/submit/', views.student_submit, name='student_submit'),
    path('student/submission/<int:submission_id>/', views.student_submission_view, name='student_submission_view'),
    path('student/submission/<int:submission_id>/delete/', views.student_submission_delete, name='student_submission_delete'),
    path('student/marks-feedback/', views.student_marks_feedback, name='student_marks_feedback'),

    # File Download
    path('download/<str:file_type>/<int:item_id>/', views.download_file, name='download_file'),
]
