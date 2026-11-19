# 🚀 SAMS (Student Assignment Management System) - Deployment Guide

This guide covers deploying the SAMS Django web application to production using **Render.com (Free & Recommended)**, **Railway**, **PythonAnywhere**, **Docker**, or a **Linux VPS (Ubuntu / Nginx)**.

---

## 📋 Pre-Deployment Checklist

Before deploying, verify that the following files are present in the project root:
- `requirements.txt` (All required dependencies including `whitenoise`, `gunicorn`, `dj-database-url`)
- `Procfile` (For Render, Railway, Heroku)
- `build.sh` (Automated build script for static collection & migrations)
- `render.yaml` (1-click Blueprint for Render)
- `Dockerfile` & `docker-compose.yml` (For container deployment)
- `.env.example` (Template for environment variables)

---

## 🌟 Method 1: Deploy to Render.com (Free, Fastest & Recommended)

Render provides free hosting for Python web services and automatically handles HTTPS SSL certificates.

### Step 1: Push Project to GitHub
1. Initialize a git repository if you haven't already:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for SAMS deployment"
   ```
2. Create a new repository on [GitHub](https://github.com/new).
3. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Create Web Service on Render
1. Go to [Render.com](https://render.com) and sign in with GitHub.
2. Click **New +** -> **Web Service**.
3. Select your SAMS repository from GitHub.
4. Fill in the details:
   - **Name**: `sams-portal` (or any custom name)
   - **Region**: Choose closest to your users (e.g., Singapore or Frankfurt)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn sams_project.wsgi:application --bind 0.0.0.0:$PORT`
   - **Instance Type**: `Free`

### Step 3: Add Environment Variables
In the **Environment Variables** section on Render, add:
| Key | Value |
|---|---|
| `PYTHON_VERSION` | `3.12.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | *(Click "Generate" or paste a random secret string)* |
| `ALLOWED_HOSTS` | `*` |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` |

5. Click **Create Web Service**.
6. Render will run `build.sh`, collect static files, run migrations, seed initial demo data, and start the Gunicorn server.
7. Your site is live at: `https://your-app-name.onrender.com`!

---

## 🚂 Method 2: Deploy to Railway.app

1. Go to [Railway.app](https://railway.app/) and sign in with GitHub.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Choose your repository.
4. In Railway project settings, add the environment variables:
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*`
   - `CSRF_TRUSTED_ORIGINS`: `https://*.railway.app`
5. Railway will automatically detect the `Procfile` and deploy your app.
6. Generate a domain under **Settings -> Networking -> Generate Domain**.

---

## 🐍 Method 3: Deploy to PythonAnywhere (Free & Simple)

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com/).
2. Open a **Bash Console** in your dashboard.
3. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git sams_project
   cd sams_project
   ```
4. Create and activate a virtualenv:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 sams-env
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   python seed_data.py
   ```
5. Go to the **Web** tab in PythonAnywhere:
   - Add a new web app (Manual configuration -> Python 3.10).
   - Set **Source code**: `/home/yourusername/sams_project`
   - Set **Virtualenv**: `/home/yourusername/.virtualenvs/sams-env`
   - In **WSGI configuration file**, replace the contents with:
     ```python
     import os
     import sys
     path = '/home/yourusername/sams_project'
     if path not in sys.path:
         sys.path.append(path)
     os.environ['DJANGO_SETTINGS_MODULE'] = 'sams_project.settings'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
   - In **Static files** section:
     - URL: `/static/` -> Directory: `/home/yourusername/sams_project/staticfiles/`
     - URL: `/media/` -> Directory: `/home/yourusername/sams_project/media/`
6. Click **Reload yourusername.pythonanywhere.com**. Done!

---

## 🐳 Method 4: Deploy with Docker & Docker Compose

For deploying on any Linux VPS (DigitalOcean, AWS EC2, Linode, Hetzner, etc.):

1. Clone your project onto the server:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd "student assignment submitiion"
   ```
2. Build and start the container in the background:
   ```bash
   docker compose up -d --build
   ```
3. Check status:
   ```bash
   docker compose logs -f
   ```
4. Your application is running on port `8000` (`http://your-server-ip:8000`).

---

## 🖥️ Method 5: Production Linux VPS (Ubuntu 22.04 / 24.04 + Nginx + Gunicorn)

### 1. System packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git
```

### 2. Setup project & virtualenv
```bash
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git sams
sudo chown -R $USER:$USER /var/www/sams
cd /var/www/sams

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python seed_data.py
```

### 3. Create Systemd Service for Gunicorn
Create file `/etc/systemd/system/sams.service`:
```ini
[Unit]
Description=Gunicorn daemon for SAMS Django Portal
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sams
ExecStart=/var/www/sams/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 sams_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl start sams
sudo systemctl enable sams
```

### 4. Configure Nginx
Create `/etc/nginx/sites-available/sams`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 15M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/sams/staticfiles/;
    }

    location /media/ {
        alias /var/www/sams/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable Nginx config:
```bash
sudo ln -s /etc/nginx/sites-available/sams /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Add Free HTTPS SSL Certificate
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## 🔑 Default Seed Accounts for Testing

Once deployed, the following demo accounts are created automatically by `seed_data.py`:

| Role | Dedicated Login URL | Username / Email | Password |
|---|---|---|---|
| **Administrator** | `/admin-panel/login/` | `admin@sams.gtu.ac.in` | `admin123` |
| **Faculty (Teacher)** | `/teacher/login/` | `priya.sharma@gtu.ac.in` | `teacher123` |
| **Student** | `/student/login/` | `shivang@student.gtu.ac.in` | `student123` |

---

## 💡 Key Production Features Included
- **Zero-Config Static Serving**: Configured with `WhiteNoise` with gzip compression and cache-busting.
- **Database Flexibility**: Supports cloud databases via `DATABASE_URL` (PostgreSQL, MySQL) or standalone SQLite fallback.
- **Secure File Uploads**: Validated file extensions (`.pdf`, `.docx`, `.zip`, `.jpg`, `.png`) up to 10MB.
- **CSRF & Security Headers**: Clickjacking protection, XSS filtering, content type sniff prevention, and HTTPS SSL compatibility.

