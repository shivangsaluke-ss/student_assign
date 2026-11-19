import os

os.makedirs('static/img/cards', exist_ok=True)
os.makedirs('static/img/diagrams', exist_ok=True)

# 1. Admin Card SVG
admin_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" fill="none">
  <defs>
    <linearGradient id="adminGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B3C49" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#0F766E" stop-opacity="0.2"/>
    </linearGradient>
  </defs>
  <rect width="380" height="200" rx="16" fill="url(#adminGrad)"/>
  <g transform="translate(50, 30)">
    <rect x="0" y="0" width="170" height="120" rx="12" fill="#0B3C49" opacity="0.95"/>
    <rect x="10" y="10" width="150" height="24" rx="6" fill="#0F766E"/>
    <circle cx="24" cy="22" r="4" fill="#E5484D"/>
    <circle cx="36" cy="22" r="4" fill="#D97706"/>
    <circle cx="48" cy="22" r="4" fill="#16A34A"/>
    <rect x="18" y="48" width="24" height="55" rx="4" fill="#0E7490" opacity="0.8"/>
    <rect x="52" y="65" width="24" height="38" rx="4" fill="#16A34A" opacity="0.9"/>
    <rect x="86" y="38" width="24" height="65" rx="4" fill="#D97706" opacity="0.9"/>
    <rect x="120" y="55" width="24" height="48" rx="4" fill="#E5484D" opacity="0.8"/>
    
    <g transform="translate(155, 40)">
      <circle cx="42" cy="42" r="38" fill="white" filter="drop-shadow(0 4px 10px rgba(11,60,73,0.2))"/>
      <path d="M42 20 L62 28 V46 C62 58 42 66 42 66 C42 66 22 58 22 46 V28 Z" fill="#0F766E"/>
      <path d="M35 43 L40 48 L50 36" stroke="white" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>
</svg>"""

with open('static/img/cards/admin_card.svg', 'w', encoding='utf-8') as f:
    f.write(admin_svg)

# 2. Teacher Card SVG
teacher_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" fill="none">
  <defs>
    <linearGradient id="teachGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F766E" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#16A34A" stop-opacity="0.2"/>
    </linearGradient>
  </defs>
  <rect width="380" height="200" rx="16" fill="url(#teachGrad)"/>
  <g transform="translate(60, 25)">
    <rect x="20" y="10" width="130" height="145" rx="10" fill="white" stroke="#CBD5E1" stroke-width="2"/>
    <rect x="55" y="2" width="60" height="16" rx="4" fill="#0B3C49"/>
    <rect x="35" y="35" width="95" height="7" rx="3.5" fill="#94A3B8"/>
    <rect x="35" y="52" width="80" height="7" rx="3.5" fill="#CBD5E1"/>
    <rect x="35" y="69" width="90" height="7" rx="3.5" fill="#CBD5E1"/>
    <rect x="35" y="86" width="65" height="7" rx="3.5" fill="#CBD5E1"/>
    
    <circle cx="110" cy="118" r="22" fill="#E5484D" fill-opacity="0.12" stroke="#E5484D" stroke-width="2.5" stroke-dasharray="4 2"/>
    <text x="100" y="125" fill="#E5484D" font-family="sans-serif" font-weight="900" font-size="19">A+</text>
    
    <g transform="translate(145, 55)">
      <circle cx="36" cy="36" r="34" fill="#0F766E" filter="drop-shadow(0 4px 8px rgba(15,118,110,0.3))"/>
      <path d="M25 36 L33 44 L48 27" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>
</svg>"""

with open('static/img/cards/teacher_card.svg', 'w', encoding='utf-8') as f:
    f.write(teacher_svg)

# 3. Student Card SVG
student_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" fill="none">
  <defs>
    <linearGradient id="studGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0E7490" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#D97706" stop-opacity="0.2"/>
    </linearGradient>
  </defs>
  <rect width="380" height="200" rx="16" fill="url(#studGrad)"/>
  <g transform="translate(55, 25)">
    <rect x="25" y="20" width="150" height="98" rx="8" fill="#1E293B" stroke="#334155" stroke-width="3"/>
    <rect x="35" y="30" width="130" height="74" rx="4" fill="#0B3C49"/>
    <polygon points="10,118 190,118 180,128 20,128" fill="#94A3B8"/>
    
    <circle cx="100" cy="62" r="20" fill="white" fill-opacity="0.2"/>
    <path d="M92 66 L100 56 L108 66 M100 56 V73" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    
    <g transform="translate(160, 10)">
      <path d="M35 15 L65 30 L35 45 L5 30 Z" fill="#0E7490"/>
      <path d="M15 35 V50 C15 58 55 58 55 50 V35" fill="#0B3C49"/>
      <line x1="65" y1="30" x2="70" y2="50" stroke="#D97706" stroke-width="2"/>
      <circle cx="70" cy="52" r="3" fill="#D97706"/>
    </g>
  </g>
</svg>"""

with open('static/img/cards/student_card.svg', 'w', encoding='utf-8') as f:
    f.write(student_svg)

# Diagrams
# 1. System Flow Diagram
system_flow_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" fill="none">
  <rect width="960" height="520" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
  <text x="480" y="45" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="24" fill="#0B3C49">SAMS: Overall System Flow &amp; Lifecycle</text>
  
  <!-- Step 1: Admin Course Setup -->
  <g transform="translate(40, 80)">
    <rect width="180" height="110" rx="10" fill="#0B3C49" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.1))"/>
    <text x="90" y="35" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FFFFFF">1. Administration</text>
    <text x="90" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#E2E8F0">Setup Semester &amp; Courses</text>
    <text x="90" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#CBD5E1">Assign Faculty to Subject</text>
  </g>

  <!-- Arrow -->
  <path d="M220 135 H 270" stroke="#0F766E" stroke-width="3" marker-end="url(#arrow)"/>

  <!-- Step 2: Teacher Creates Assignment -->
  <g transform="translate(270, 80)">
    <rect width="190" height="110" rx="10" fill="#0F766E" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.1))"/>
    <text x="95" y="35" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FFFFFF">2. Assignment Posting</text>
    <text x="95" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#E2E8F0">Define Topic &amp; Criteria</text>
    <text x="95" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#CBD5E1">Set Strict Due Date</text>
  </g>

  <!-- Arrow -->
  <path d="M460 135 H 510" stroke="#0F766E" stroke-width="3"/>

  <!-- Step 3: Student Submission -->
  <g transform="translate(510, 80)">
    <rect width="190" height="110" rx="10" fill="#0E7490" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.1))"/>
    <text x="95" y="35" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FFFFFF">3. Student Submission</text>
    <text x="95" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#E2E8F0">Upload Solution Document</text>
    <text x="95" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#CBD5E1">Status: Submitted / Late</text>
  </g>

  <!-- Arrow -->
  <path d="M700 135 H 740" stroke="#0F766E" stroke-width="3"/>

  <!-- Step 4: Teacher Evaluation -->
  <g transform="translate(740, 80)">
    <rect width="180" height="110" rx="10" fill="#D97706" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.1))"/>
    <text x="90" y="35" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FFFFFF">4. Faculty Grading</text>
    <text x="90" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#FEF3C7">Review Document</text>
    <text x="90" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#FEF3C7">Award Marks &amp; Feedback</text>
  </g>

  <!-- Return Flow Down -->
  <path d="M830 190 V 270 H 480" stroke="#16A34A" stroke-width="3" stroke-dasharray="6 4"/>

  <!-- Step 5: Returned & Student Analytics -->
  <g transform="translate(320, 270)">
    <rect width="320" height="100" rx="10" fill="#16A34A" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.1))"/>
    <text x="160" y="35" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FFFFFF">5. Marks Published &amp; Returned</text>
    <text x="160" y="60" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#DCFCE7">Student views remarks, marks, and peer standing</text>
    <text x="160" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#DCFCE7">Automated status upgrade to 'Returned'</text>
  </g>

  <!-- Step 6: Reports & Audit -->
  <g transform="translate(80, 400)">
    <rect width="800" height="85" rx="10" fill="#FFFFFF" stroke="#0B3C49" stroke-width="2"/>
    <text x="400" y="32" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0B3C49">Administrative Audit &amp; Performance Insights</text>
    <text x="400" y="58" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#64748B">Course submission rates, late submissions metrics, teacher evaluation velocity &amp; student mark distributions</text>
  </g>
</svg>"""

with open('static/img/diagrams/system_flow.svg', 'w', encoding='utf-8') as f:
    f.write(system_flow_svg)

# 2. Use Case Diagram
use_case_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" fill="none">
  <rect width="960" height="560" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
  <text x="480" y="40" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="24" fill="#0B3C49">SAMS: System Use-Case Diagram</text>

  <!-- System boundary -->
  <rect x="230" y="60" width="500" height="470" rx="12" fill="white" stroke="#0B3C49" stroke-width="2" stroke-dasharray="4 2"/>
  <text x="480" y="85" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="16" fill="#0B3C49">Student Assignment Management System Boundary</text>

  <!-- Actor: Admin -->
  <g transform="translate(80, 110)">
    <circle cx="30" cy="25" r="18" fill="#0B3C49"/>
    <line x1="30" y1="43" x2="30" y2="90" stroke="#0B3C49" stroke-width="4"/>
    <line x1="5" y1="60" x2="55" y2="60" stroke="#0B3C49" stroke-width="4"/>
    <line x1="30" y1="90" x2="10" y2="125" stroke="#0B3C49" stroke-width="4"/>
    <line x1="30" y1="90" x2="50" y2="125" stroke="#0B3C49" stroke-width="4"/>
    <text x="30" y="145" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0B3C49">Admin</text>
  </g>

  <!-- Actor: Student -->
  <g transform="translate(80, 340)">
    <circle cx="30" cy="25" r="18" fill="#0E7490"/>
    <line x1="30" y1="43" x2="30" y2="90" stroke="#0E7490" stroke-width="4"/>
    <line x1="5" y1="60" x2="55" y2="60" stroke="#0E7490" stroke-width="4"/>
    <line x1="30" y1="90" x2="10" y2="125" stroke="#0E7490" stroke-width="4"/>
    <line x1="30" y1="90" x2="50" y2="125" stroke="#0E7490" stroke-width="4"/>
    <text x="30" y="145" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0E7490">Student</text>
  </g>

  <!-- Actor: Teacher -->
  <g transform="translate(820, 220)">
    <circle cx="30" cy="25" r="18" fill="#0F766E"/>
    <line x1="30" y1="43" x2="30" y2="90" stroke="#0F766E" stroke-width="4"/>
    <line x1="5" y1="60" x2="55" y2="60" stroke="#0F766E" stroke-width="4"/>
    <line x1="30" y1="90" x2="10" y2="125" stroke="#0F766E" stroke-width="4"/>
    <line x1="30" y1="90" x2="50" y2="125" stroke="#0F766E" stroke-width="4"/>
    <text x="30" y="145" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0F766E">Teacher</text>
  </g>

  <!-- Use cases (oavals) -->
  <g transform="translate(270, 105)">
    <ellipse cx="100" cy="25" rx="95" ry="22" fill="#F1F5F9" stroke="#0B3C49" stroke-width="1.5"/>
    <text x="100" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0F172A">Manage Courses &amp; Teachers</text>
  </g>
  <g transform="translate(270, 165)">
    <ellipse cx="100" cy="25" rx="95" ry="22" fill="#F1F5F9" stroke="#0B3C49" stroke-width="1.5"/>
    <text x="100" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0F172A">Enroll Students &amp; View Audit</text>
  </g>
  <g transform="translate(270, 225)">
    <ellipse cx="100" cy="25" rx="95" ry="22" fill="#F1F5F9" stroke="#0F766E" stroke-width="1.5"/>
    <text x="100" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0F172A">Create &amp; Update Assignments</text>
  </g>
  <g transform="translate(500, 225)">
    <ellipse cx="100" cy="25" rx="95" ry="22" fill="#F1F5F9" stroke="#0F766E" stroke-width="1.5"/>
    <text x="100" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0F172A">Grade &amp; Give Feedback</text>
  </g>
  <g transform="translate(270, 290)">
    <ellipse cx="100" cy="25" rx="95" ry="22" fill="#F1F5F9" stroke="#0E7490" stroke-width="1.5"/>
    <text x="100" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0F172A">Upload &amp; Resubmit Assignment</text>
  </g>
  <g transform="translate(270, 355)">
    <ellipse cx="100" cy="25" rx="95" ry="22" fill="#F1F5F9" stroke="#0E7490" stroke-width="1.5"/>
    <text x="100" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0F172A">View Feedback &amp; Marks</text>
  </g>
  <g transform="translate(380, 420)">
    <ellipse cx="100" cy="25" rx="95" ry="22" fill="#FEF3C7" stroke="#D97706" stroke-width="1.5"/>
    <text x="100" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#B45309">Authenticate (Login / Register)</text>
  </g>

  <!-- Connectors -->
  <line x1="140" y1="160" x2="270" y2="130" stroke="#0B3C49" stroke-width="1.5"/>
  <line x1="140" y1="160" x2="270" y2="190" stroke="#0B3C49" stroke-width="1.5"/>
  <line x1="140" y1="160" x2="380" y2="445" stroke="#0B3C49" stroke-width="1.5"/>

  <line x1="140" y1="390" x2="270" y2="315" stroke="#0E7490" stroke-width="1.5"/>
  <line x1="140" y1="390" x2="270" y2="380" stroke="#0E7490" stroke-width="1.5"/>
  <line x1="140" y1="390" x2="380" y2="445" stroke="#0E7490" stroke-width="1.5"/>

  <line x1="820" y1="270" x2="470" y2="250" stroke="#0F766E" stroke-width="1.5"/>
  <line x1="820" y1="270" x2="700" y2="250" stroke="#0F766E" stroke-width="1.5"/>
  <line x1="820" y1="270" x2="580" y2="445" stroke="#0F766E" stroke-width="1.5"/>
</svg>"""

with open('static/img/diagrams/use_case.svg', 'w', encoding='utf-8') as f:
    f.write(use_case_svg)

# 3. Class Diagram SVG
class_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 620" fill="none">
  <rect width="960" height="620" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
  <text x="480" y="35" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="22" fill="#0B3C49">SAMS: UML Class Diagram (8 Core Entities)</text>

  <!-- Class 1: Admin -->
  <g transform="translate(30, 60)">
    <rect width="180" height="130" rx="6" fill="white" stroke="#0B3C49" stroke-width="2"/>
    <rect width="180" height="28" rx="6" fill="#0B3C49"/>
    <text x="90" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Admin</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ admin_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ admin_name : str</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ admin_email : str</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ admin_password : str</text>
    <text x="10" y="120" font-family="monospace" font-size="10" fill="#334155">+ admin_mobile : str</text>
  </g>

  <!-- Class 2: Teacher -->
  <g transform="translate(260, 60)">
    <rect width="190" height="130" rx="6" fill="white" stroke="#0F766E" stroke-width="2"/>
    <rect width="190" height="28" rx="6" fill="#0F766E"/>
    <text x="95" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Teacher</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ teacher_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ teacher_name : str</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ teacher_email : str</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ department : str</text>
    <text x="10" y="120" font-family="monospace" font-size="10" fill="#334155">+ teacher_password : str</text>
  </g>

  <!-- Class 3: Course -->
  <g transform="translate(500, 60)">
    <rect width="190" height="130" rx="6" fill="white" stroke="#0E7490" stroke-width="2"/>
    <rect width="190" height="28" rx="6" fill="#0E7490"/>
    <text x="95" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Course</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ course_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ course_name : str</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ teacher_id : int (FK)</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ semester : int</text>
  </g>

  <!-- Class 4: Assignment -->
  <g transform="translate(730, 60)">
    <rect width="200" height="150" rx="6" fill="white" stroke="#D97706" stroke-width="2"/>
    <rect width="200" height="28" rx="6" fill="#D97706"/>
    <text x="100" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Assignment</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ assignment_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ title : str</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ description : text</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ course_id : int (FK)</text>
    <text x="10" y="120" font-family="monospace" font-size="10" fill="#334155">+ due_date : datetime</text>
    <text x="10" y="138" font-family="monospace" font-size="10" fill="#334155">+ max_marks : int</text>
  </g>

  <!-- Class 5: Student -->
  <g transform="translate(30, 260)">
    <rect width="190" height="145" rx="6" fill="white" stroke="#0E7490" stroke-width="2"/>
    <rect width="190" height="28" rx="6" fill="#0E7490"/>
    <text x="95" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Student</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ student_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ student_name : str</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ student_email : str</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ roll_no : str</text>
    <text x="10" y="120" font-family="monospace" font-size="10" fill="#334155">+ semester : int</text>
    <text x="10" y="138" font-family="monospace" font-size="10" fill="#334155">+ student_password : str</text>
  </g>

  <!-- Class 6: Enrollment -->
  <g transform="translate(260, 260)">
    <rect width="190" height="120" rx="6" fill="white" stroke="#16A34A" stroke-width="2"/>
    <rect width="190" height="28" rx="6" fill="#16A34A"/>
    <text x="95" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Enrollment</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ enroll_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ student_id : int (FK)</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ course_id : int (FK)</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ enroll_date : date</text>
  </g>

  <!-- Class 7: Submission -->
  <g transform="translate(500, 260)">
    <rect width="190" height="150" rx="6" fill="white" stroke="#E5484D" stroke-width="2"/>
    <rect width="190" height="28" rx="6" fill="#E5484D"/>
    <text x="95" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Submission</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ submission_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ assignment_id : int (FK)</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ student_id : int (FK)</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ file_path : str</text>
    <text x="10" y="120" font-family="monospace" font-size="10" fill="#334155">+ submitted_at : datetime</text>
    <text x="10" y="138" font-family="monospace" font-size="10" fill="#334155">+ status : str</text>
  </g>

  <!-- Class 8: Evaluation -->
  <g transform="translate(730, 260)">
    <rect width="200" height="130" rx="6" fill="white" stroke="#0F766E" stroke-width="2"/>
    <rect width="200" height="28" rx="6" fill="#0F766E"/>
    <text x="100" y="19" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Evaluation</text>
    <text x="10" y="48" font-family="monospace" font-size="10" fill="#334155">+ evaluation_id : int (PK)</text>
    <text x="10" y="66" font-family="monospace" font-size="10" fill="#334155">+ submission_id : int (FK/UNI)</text>
    <text x="10" y="84" font-family="monospace" font-size="10" fill="#334155">+ marks : int</text>
    <text x="10" y="102" font-family="monospace" font-size="10" fill="#334155">+ feedback : str</text>
    <text x="10" y="120" font-family="monospace" font-size="10" fill="#334155">+ evaluated_on : date</text>
  </g>

  <!-- Cardinality Lines -->
  <!-- Teacher 1:N Course -->
  <line x1="450" y1="125" x2="500" y2="125" stroke="#334155" stroke-width="2"/>
  <text x="455" y="115" font-family="sans-serif" font-size="11" fill="#64748B">1</text>
  <text x="485" y="115" font-family="sans-serif" font-size="11" fill="#64748B">N</text>

  <!-- Course 1:N Assignment -->
  <line x1="690" y1="125" x2="730" y2="125" stroke="#334155" stroke-width="2"/>
  <text x="695" y="115" font-family="sans-serif" font-size="11" fill="#64748B">1</text>
  <text x="715" y="115" font-family="sans-serif" font-size="11" fill="#64748B">N</text>

  <!-- Student 1:N Enrollment & Course 1:N Enrollment -->
  <line x1="220" y1="320" x2="260" y2="320" stroke="#334155" stroke-width="2"/>
  <text x="225" y="310" font-family="sans-serif" font-size="11" fill="#64748B">1</text>
  <text x="245" y="310" font-family="sans-serif" font-size="11" fill="#64748B">N</text>

  <!-- Assignment 1:N Submission -->
  <line x1="730" y1="190" x2="690" y2="280" stroke="#334155" stroke-width="2"/>
  <text x="735" y="210" font-family="sans-serif" font-size="11" fill="#64748B">1</text>
  <text x="695" y="260" font-family="sans-serif" font-size="11" fill="#64748B">N</text>

  <!-- Submission 1:1 Evaluation -->
  <line x1="690" y1="325" x2="730" y2="325" stroke="#334155" stroke-width="2"/>
  <text x="695" y="315" font-family="sans-serif" font-size="11" fill="#64748B">1</text>
  <text x="715" y="315" font-family="sans-serif" font-size="11" fill="#64748B">1</text>
</svg>"""

with open('static/img/diagrams/class_diagram.svg', 'w', encoding='utf-8') as f:
    f.write(class_svg)

# 4. Sequence Diagram SVG
sequence_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" fill="none">
  <rect width="960" height="540" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
  <text x="480" y="35" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="22" fill="#0B3C49">SAMS: Assignment &amp; Grading Sequence</text>

  <!-- Lifeline headers -->
  <rect x="80" y="60" width="120" height="40" rx="8" fill="#0F766E"/>
  <text x="140" y="85" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Teacher</text>
  
  <rect x="360" y="60" width="120" height="40" rx="8" fill="#0B3C49"/>
  <text x="420" y="85" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">SAMS Core</text>

  <rect x="680" y="60" width="120" height="40" rx="8" fill="#0E7490"/>
  <text x="740" y="85" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="13" fill="white">Student</text>

  <!-- Lifelines -->
  <line x1="140" y1="100" x2="140" y2="500" stroke="#94A3B8" stroke-width="2" stroke-dasharray="6 4"/>
  <line x1="420" y1="100" x2="420" y2="500" stroke="#94A3B8" stroke-width="2" stroke-dasharray="6 4"/>
  <line x1="740" y1="100" x2="740" y2="500" stroke="#94A3B8" stroke-width="2" stroke-dasharray="6 4"/>

  <!-- Messages -->
  <!-- 1. Post Assignment -->
  <line x1="140" y1="140" x2="420" y2="140" stroke="#0F766E" stroke-width="2"/>
  <polygon points="420,140 410,135 410,145" fill="#0F766E"/>
  <text x="280" y="132" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0F766E">1. Create Assignment(due_date, marks)</text>

  <!-- 2. Notification -->
  <line x1="420" y1="180" x2="740" y2="180" stroke="#0E7490" stroke-width="2"/>
  <polygon points="740,180 730,175 730,185" fill="#0E7490"/>
  <text x="580" y="172" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0E7490">2. Notify Enrolled Students</text>

  <!-- 3. Submit Document -->
  <line x1="740" y1="230" x2="420" y2="230" stroke="#0B3C49" stroke-width="2"/>
  <polygon points="420,230 430,225 430,235" fill="#0B3C49"/>
  <text x="580" y="222" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#0B3C49">3. Upload Solution File (PDF/DOCX)</text>

  <!-- Internal validation -->
  <rect x="400" y="250" width="40" height="35" rx="4" fill="#E2E8F0"/>
  <text x="420" y="272" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#475569">Validate File &amp; Due Date</text>

  <!-- 4. Review & Grade -->
  <line x1="140" y1="320" x2="420" y2="320" stroke="#D97706" stroke-width="2"/>
  <polygon points="420,320 410,315 410,325" fill="#D97706"/>
  <text x="280" y="312" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#D97706">4. Submit Grade(marks, feedback)</text>

  <!-- 5. Status Evaluated -->
  <line x1="420" y1="370" x2="420" y2="390" stroke="#16A34A" stroke-width="2"/>
  <text x="470" y="385" font-family="sans-serif" font-size="11" fill="#16A34A">Status &lt;- Evaluated</text>

  <!-- 6. Return Result -->
  <line x1="420" y1="420" x2="740" y2="420" stroke="#16A34A" stroke-width="2"/>
  <polygon points="740,420 730,415 730,425" fill="#16A34A"/>
  <text x="580" y="412" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#16A34A">5. Return Marks &amp; Feedback</text>

  <!-- 7. Status Returned -->
  <line x1="740" y1="460" x2="420" y2="460" stroke="#64748B" stroke-width="2" stroke-dasharray="4 2"/>
  <polygon points="420,460 430,455 430,465" fill="#64748B"/>
  <text x="580" y="452" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#64748B">6. Acknowledge (Status &lt;- Returned)</text>
</svg>"""

with open('static/img/diagrams/sequence_diagram.svg', 'w', encoding='utf-8') as f:
    f.write(sequence_svg)

# 5. ER Diagram SVG
er_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 620" fill="none">
  <rect width="960" height="620" rx="16" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
  <text x="480" y="35" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="22" fill="#0B3C49">SAMS: Entity-Relationship (ER) Diagram</text>

  <!-- Table 1: admin -->
  <g transform="translate(40, 60)">
    <rect width="180" height="135" rx="6" fill="white" stroke="#0B3C49" stroke-width="2"/>
    <rect width="180" height="26" rx="6" fill="#0B3C49"/>
    <text x="90" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">admin</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | admin_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">   | admin_name</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">U  | admin_email</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">   | admin_password</text>
    <text x="10" y="118" font-family="sans-serif" font-size="11" fill="#0F172A">U  | admin_mobile</text>
  </g>

  <!-- Table 2: teacher -->
  <g transform="translate(260, 60)">
    <rect width="190" height="135" rx="6" fill="white" stroke="#0F766E" stroke-width="2"/>
    <rect width="190" height="26" rx="6" fill="#0F766E"/>
    <text x="95" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">teacher</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | teacher_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">   | teacher_name</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">U  | teacher_email</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">   | department</text>
    <text x="10" y="118" font-family="sans-serif" font-size="11" fill="#0F172A">   | teacher_password</text>
  </g>

  <!-- Table 3: course -->
  <g transform="translate(500, 60)">
    <rect width="190" height="120" rx="6" fill="white" stroke="#0E7490" stroke-width="2"/>
    <rect width="190" height="26" rx="6" fill="#0E7490"/>
    <text x="95" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">course</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | course_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">   | course_name</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">FK | teacher_id</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">   | semester</text>
  </g>

  <!-- Table 4: assignment -->
  <g transform="translate(730, 60)">
    <rect width="190" height="155" rx="6" fill="white" stroke="#D97706" stroke-width="2"/>
    <rect width="190" height="26" rx="6" fill="#D97706"/>
    <text x="95" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">assignment</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | assignment_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">   | title</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">   | description</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">FK | course_id</text>
    <text x="10" y="118" font-family="sans-serif" font-size="11" fill="#0F172A">IX | due_date</text>
    <text x="10" y="136" font-family="sans-serif" font-size="11" fill="#0F172A">   | max_marks</text>
  </g>

  <!-- Table 5: student -->
  <g transform="translate(40, 260)">
    <rect width="180" height="150" rx="6" fill="white" stroke="#0E7490" stroke-width="2"/>
    <rect width="180" height="26" rx="6" fill="#0E7490"/>
    <text x="90" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">student</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | student_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">   | student_name</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">U  | student_email</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">U  | roll_no</text>
    <text x="10" y="118" font-family="sans-serif" font-size="11" fill="#0F172A">   | semester</text>
    <text x="10" y="136" font-family="sans-serif" font-size="11" fill="#0F172A">   | student_password</text>
  </g>

  <!-- Table 6: enrollment -->
  <g transform="translate(260, 260)">
    <rect width="190" height="120" rx="6" fill="white" stroke="#16A34A" stroke-width="2"/>
    <rect width="190" height="26" rx="6" fill="#16A34A"/>
    <text x="95" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">enrollment</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | enroll_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">FK | student_id</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">FK | course_id</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">   | enroll_date</text>
  </g>

  <!-- Table 7: submission -->
  <g transform="translate(500, 260)">
    <rect width="190" height="150" rx="6" fill="white" stroke="#E5484D" stroke-width="2"/>
    <rect width="190" height="26" rx="6" fill="#E5484D"/>
    <text x="95" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">submission</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | submission_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">FK | assignment_id</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">FK | student_id</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">   | file_path</text>
    <text x="10" y="118" font-family="sans-serif" font-size="11" fill="#0F172A">   | submitted_at</text>
    <text x="10" y="136" font-family="sans-serif" font-size="11" fill="#0F172A">   | status</text>
  </g>

  <!-- Table 8: evaluation -->
  <g transform="translate(730, 260)">
    <rect width="190" height="135" rx="6" fill="white" stroke="#0F766E" stroke-width="2"/>
    <rect width="190" height="26" rx="6" fill="#0F766E"/>
    <text x="95" y="18" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="12" fill="white">evaluation</text>
    <text x="10" y="46" font-family="sans-serif" font-size="11" fill="#0F172A">PK | evaluation_id</text>
    <text x="10" y="64" font-family="sans-serif" font-size="11" fill="#0F172A">FK | submission_id (UNI)</text>
    <text x="10" y="82" font-family="sans-serif" font-size="11" fill="#0F172A">   | marks</text>
    <text x="10" y="100" font-family="sans-serif" font-size="11" fill="#0F172A">   | feedback</text>
    <text x="10" y="118" font-family="sans-serif" font-size="11" fill="#0F172A">   | evaluated_on</text>
  </g>
</svg>"""

with open('static/img/diagrams/er_diagram.svg', 'w', encoding='utf-8') as f:
    f.write(er_svg)

print('All SVGs generated successfully.')
