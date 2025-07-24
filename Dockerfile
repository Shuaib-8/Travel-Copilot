FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
  && apt-get -y install g++ ca-certificates curl gnupg \
  && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/ 
COPY requirements-dev.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
