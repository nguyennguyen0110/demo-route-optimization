# Use a smaller base image with Python pre-installed
FROM python:3.12.3-slim

# Set working directory inside the container
WORKDIR /app

# Expose port
EXPOSE 8080

# Create virtual environment
RUN python -m venv venv

# Ensure pip is up to date in the venv
RUN venv/bin/pip install --upgrade pip

# Copy requirements and install them inside the venv
COPY requirements.txt .
RUN venv/bin/pip install -r requirements.txt

# Copy all application files
COPY . .

# Start the application using gunicorn inside the venv
CMD ["venv/bin/gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "-t", "120", "app:app"]
