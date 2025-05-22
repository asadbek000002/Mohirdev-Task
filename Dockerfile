# Base image
FROM python:3.10

# Working directory
WORKDIR /intakehub

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install Python dependencies
COPY requirements.txt /intakehub/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Create and set permissions for staticfiles & mediafiles folders
RUN mkdir -p /intakehub/staticfiles /intakehub/mediafiles
RUN chmod 755 /intakehub/staticfiles /intakehub/mediafiles

# Copy project files
COPY . /intakehub/


# Expose port
EXPOSE 8000

# Run migrations and start Daphne server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 intakehub.wsgi:application"]



