#!/usr/bin/env bash
# SAMS Automated Cloud Build & Deployment Script
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> [1/4] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> [2/4] Collecting static assets with WhiteNoise compression..."
python manage.py collectstatic --no-input

echo "==> [3/4] Running database migrations..."
python manage.py migrate --no-input

echo "==> [4/4] Seeding initial demo data (Admin, Faculty, Students, Courses)..."
python seed_data.py

echo "==> SAMS deployment build completed successfully!"

