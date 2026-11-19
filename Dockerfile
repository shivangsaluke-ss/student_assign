# Use official Python lightweight image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies (build-essential, libmariadb-dev for mysql client if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose server port
EXPOSE 8000

# Run gunicorn server
CMD ["sh", "-c", "python manage.py migrate --no-input && python seed_data.py && gunicorn sams_project.wsgi:application --bind 0.0.0.0:${PORT}"]

