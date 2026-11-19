<<<<<<< HEAD
# Student Assignment Management System (SAMS)
> **"Submit Smart. Grade Faster."**  
> *BCA Semester 5 (GTU) Minor Project — System Analysis & Design (SAD)*

---

## 1. Project Overview
The **Student Assignment Management System (SAMS)** is an integrated, role-based academic portal that replaces manual paper submissions, fragmented messaging groups, and spreadsheet tracking. Designed specifically for university faculty and students, SAMS enforces structured submission deadlines, automatic late-submission detection, role-segregated dashboards, and transparent grading with constructive teacher remarks.

### Key Highlights
- **Single Portal for 3 Roles:** Administrator, Teacher, and Student with strict `@admin_required`, `@teacher_required`, and `@student_required` authorization decorators.
- **Visual Design Reference:** Faithfully translated from `reference/design.mp4` with custom design tokens (`DESIGN.md`), glassmorphic styling, cosmic gradient canvas, and responsive mobile adaptations (≤ 820px).
- **8 Normalized MySQL Tables:** Exact relational schema with primary keys, indexed foreign keys, and referential integrity constraints.
- **5-Stage Submission Lifecycle:** Color-coded badges for **Pending**, **Submitted**, **Late**, **Evaluated**, and **Returned** states.
- **Automated Validation:** Client and server-side file upload inspection (PDF, DOC, DOCX, ZIP, JPG, PNG; max 10MB) and numerical marks validation ($0 \le \text{marks} \le \text{max\_marks}$).

---

## 2. Project Team & Mentorship
- **Dishant Jain** (Roll No: 3031, Contact: +91 96622 66942)
- **Mehul Jain** (Roll No: 3032, Contact: +91 95583 61283)
- **Shivang Saluke** (Roll No: 3092, Contact: +91 97370 81972)

**Mentorship Company Profile:**
- **Company:** Akash Technolabs
- **Website:** [www.akashtechnolabs.com](http://www.akashtechnolabs.com)
- **Contact:** +91 99786 21654
- **Address:** 202 Aarya Arcade, Mithakali Six Road, Ahmedabad, Gujarat

---

## 3. Demo Credentials

| Role | Username / Email | Password | Access Portal |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` (or `admin@gtu.ac.in`) | `admin123` | `/admin-panel/` |
| **Faculty Teacher** | `anita.sharma@gtu.ac.in` (or `teacher_anita`) | `teacher123` | `/teacher/` |
| **Faculty Teacher** | `vikram.mehta@gtu.ac.in` (or `teacher_vikram`) | `teacher123` | `/teacher/` |
| **Faculty Teacher** | `neha.patel@gtu.ac.in` (or `teacher_neha`) | `teacher123` | `/teacher/` |
| **Student** | `shivang@student.gtu.ac.in` (or `std_3092`) | `student123` | `/student/` |
| **Student** | `dishant@student.gtu.ac.in` (or `std_3031`) | `student123` | `/student/` |
| **Student** | `mehul@student.gtu.ac.in` (or `std_3032`) | `student123` | `/student/` |

> *Tip: The public `/login/` page includes 1-click demo filler buttons to instantly test any of the 3 roles.*

---

## 4. Technology Stack
- **Framework:** Python 3.11+, Django 5
- **Database:** MySQL Server 9.x (`PyMySQL` / `mysqlclient`)
- **Front-End:** HTML5, CSS3 Custom Properties (Design Tokens), Vanilla JavaScript (ES6+), Bootstrap 5
- **Animations:** CSS3 Keyframes & Web Animations API
- **Fonts:** Self-hosted `Inter` & `Grandstander` in `static/fonts/`

---

## 5. Database Architecture (8 MySQL Tables)

1. `admin` (PK: `admin_id`, `admin_name`, `admin_email` UNIQUE, `admin_password`, `admin_mobile` UNIQUE)
2. `teacher` (PK: `teacher_id`, `teacher_name`, `teacher_email` UNIQUE, `department`, `teacher_password`)
3. `student` (PK: `student_id`, `student_name`, `student_email` UNIQUE, `roll_no` UNIQUE, `semester`, `student_password`)
4. `course` (PK: `course_id`, `course_name`, FK: `teacher_id`, `semester`)
5. `enrollment` (PK: `enroll_id`, FK: `student_id`, FK: `course_id`, `enroll_date` DEFAULT Today; UNIQUE `(student_id, course_id)`)
6. `assignment` (PK: `assignment_id`, `title`, `description`, FK: `course_id`, `due_date` INDEXED, `max_marks`, `file_path` OPTIONAL)
7. `submission` (PK: `submission_id`, FK: `assignment_id`, FK: `student_id`, `file_path`, `submitted_at`, `status`; UNIQUE `(assignment_id, student_id)`)
8. `evaluation` (PK: `evaluation_id`, FK: `submission_id` UNIQUE, `marks`, `feedback`, `evaluated_on` DEFAULT Today)

---

## 6. Installation & Setup Instructions

### 1. Clone & Set Up Environment
```bash
# Clone the repository and navigate into project
cd "s:\project\student assignment\2nd try"

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration (`.env`)
Create a `.env` file (refer to `.env.example`):
```env
SECRET_KEY=django-insecure-sams-gtu-bca-sem5-minor-project-key-2026-v2
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,*

DB_ENGINE=django.db.backends.mysql
DB_NAME=sams_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3308
```

### 3. Apply Database Migrations
```bash
python manage.py makemigrations sams_app
python manage.py migrate
```

### 4. Seed Demo Data
Populates the database with 1 admin, 3 teachers, 12 students, 4 courses, enrollments, 6 assignments, and submissions in all lifecycle states:
```bash
python manage.py seed_demo
```

### 5. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 6. Run Automated Test Suite
```bash
python manage.py test
```

### 7. Launch Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

---

## 7. Submission Lifecycle & Business Rules
1. **Enrollment Check:** Students can only submit to courses in which they are actively enrolled.
2. **On-Time vs Late:** Submissions received before `due_date` are marked **Submitted**. Uploads after `due_date` are automatically marked **Late**.
3. **Resubmissions:** Students may replace or delete their submitted work at any time before the deadline, provided the assignment has not yet been graded.
4. **Grading & Return:** When a teacher reviews a submission, they award marks ($0$ to `max_marks`) and enter feedback, transitioning status to **Evaluated**. When the student logs in and reviews their marks, the status transitions to **Returned**.
5. **Role Security:** Accessing another role's endpoint directly returns HTTP 403 Forbidden with a styled cosmic error template.
=======
# student_assign
>>>>>>> 34f461d5a64b34588d3efb81b7146ce778d049b1
