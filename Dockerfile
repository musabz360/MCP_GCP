# Use an official Python runtime as a parent image that supports Python 3.10 or newer.
FROM python:3.10-slim

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy the requirements.txt file into the container's /app directory.
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt (now includes Flask and gunicorn).
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory (your app.py, server.py, main.py, etc.)
# into the container's /app directory.
COPY . .

# Expose port 8080.
EXPOSE 8080

# Command to run your Flask application using Gunicorn.
# "main:app" means: look for a file named 'main.py' and within it, find a Flask application instance named 'app'.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"] # <--- MODIFIED THIS LINE