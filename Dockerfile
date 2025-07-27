FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=1
ENV DJANGO_SETTINGS_MODULE=travel_copilot.settings

# Set work directory
WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update \
    && apt-get -y install g++ ca-certificates curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Install Python dependencies
# Copy project files needed for pip install
COPY ./pyproject.toml /app/
COPY ./core/ /app/core/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e ".[dev]"

# Copy package files for Node.js dependencies
COPY package.json package-lock.json /app/
# Install all dependencies including devDependencies (needed for tailwindcss)
RUN npm ci

# Copy source files needed for build
COPY static/ /app/static/
COPY tailwind.config.js /app/
COPY travel_app/templates/ /app/travel_app/templates/

# Build static assets (Tailwind, etc.)
RUN npm run build

# Copy the rest of the project
COPY . /app/

# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Build static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
