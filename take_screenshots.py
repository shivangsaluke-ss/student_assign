import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

os.makedirs('screenshots', exist_ok=True)

def get_driver(width=1280, height=800):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument(f'--window-size={width},{height}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--hide-scrollbars')
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(options=options)
    return driver

base_url = "http://127.0.0.1:8000"

print("Capturing Public Pages...")
driver = get_driver(1280, 850)

pages = [
    ('/', '01_home.png'),
    ('/about/', '02_about.png'),
    ('/modules/', '03_modules.png'),
    ('/diagrams/', '04_diagrams.png'),
    ('/database/', '05_database.png'),
    ('/team/', '06_team.png'),
    ('/login/', '07_login.png'),
    ('/register/', '08_register.png'),
]

for path, fname in pages:
    driver.get(f"{base_url}{path}")
    time.sleep(1)
    driver.save_screenshot(f"screenshots/{fname}")
    print(f"Captured {fname}")

driver.quit()

# Mobile Viewport (≤ 820px, e.g. 390x844)
print("\nCapturing Mobile Viewport...")
m_driver = get_driver(390, 844)
m_driver.get(f"{base_url}/")
time.sleep(1)
m_driver.save_screenshot("screenshots/09_mobile_home.png")
print("Captured 09_mobile_home.png")
m_driver.quit()

# Capturing Authenticated Pages
print("\nCapturing Authenticated Portals...")

# 1. Admin
driver = get_driver(1280, 850)
driver.get(f"{base_url}/login/")
time.sleep(0.5)
driver.find_element(By.ID, "id_username").send_keys("admin")
driver.find_element(By.ID, "id_password").send_keys("admin123")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(1)
driver.save_screenshot("screenshots/10_admin_dashboard.png")
print("Captured 10_admin_dashboard.png")

driver.get(f"{base_url}/admin-panel/reports/")
time.sleep(1)
driver.save_screenshot("screenshots/11_admin_reports.png")
print("Captured 11_admin_reports.png")
driver.quit()

# 2. Teacher
driver = get_driver(1280, 850)
driver.get(f"{base_url}/login/")
time.sleep(0.5)
driver.find_element(By.ID, "id_username").send_keys("anita.sharma@gtu.ac.in")
driver.find_element(By.ID, "id_password").send_keys("teacher123")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(1)
driver.save_screenshot("screenshots/12_teacher_dashboard.png")
print("Captured 12_teacher_dashboard.png")

driver.get(f"{base_url}/teacher/submissions/")
time.sleep(1)
driver.save_screenshot("screenshots/13_teacher_submissions.png")
print("Captured 13_teacher_submissions.png")
driver.quit()

# 3. Student
driver = get_driver(1280, 850)
driver.get(f"{base_url}/login/")
time.sleep(0.5)
driver.find_element(By.ID, "id_username").send_keys("shivang@student.gtu.ac.in")
driver.find_element(By.ID, "id_password").send_keys("student123")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(1)
driver.save_screenshot("screenshots/14_student_dashboard.png")
print("Captured 14_student_dashboard.png")

driver.get(f"{base_url}/student/assignments/")
time.sleep(1)
driver.save_screenshot("screenshots/15_student_assignments.png")
print("Captured 15_student_assignments.png")

driver.get(f"{base_url}/student/submit/4/")
time.sleep(1)
driver.save_screenshot("screenshots/16_student_submit.png")
print("Captured 16_student_submit.png")

driver.get(f"{base_url}/student/grades/")
time.sleep(1)
driver.save_screenshot("screenshots/17_student_grades.png")
print("Captured 17_student_grades.png")
driver.quit()

print("\nAll screenshots captured successfully!")
