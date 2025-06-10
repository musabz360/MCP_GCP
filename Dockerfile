# Use an official Python runtime as a parent image.
# This provides a base operating system and Python pre-installed.
FROM python:3.9-slim

# Set the working directory inside the container to /app.
# All subsequent commands will run from this directory.
WORKDIR /app

# Copy the requirements.txt file into the container's /app directory.
# We do this separately so Docker can cache this layer. If requirements.txt
# doesn't change, Docker won't re-run pip install on subsequent builds,
# which speeds up builds.
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt.
# --no-cache-dir saves space by not caching pip packages.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory (your app.py, server.py, etc.)
# into the container's /app directory.
COPY . .

# Expose port 8080. This tells Docker that the container will listen on this port.
# Cloud Run expects your app to listen on 8080 by default.
EXPOSE 8080

# Command to run your MCP server (server.py).
# This will execute server.py, which will then start the FastMCP server
# listening on the PORT environment variable provided by Cloud Run (defaulting to 8080).
CMD ["python", "server.py"]