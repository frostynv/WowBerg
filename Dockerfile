FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

# Create non-root user with configuration:
    # - Username: wowberg
    # - UID: 1000 (to match typical host user permissions)
    # - Home directory: /home/wowberg
    # - Ownership of /app directory to ensure proper permissions for the non-root user
    # - This setup allows the application to run with non-root privileges while maintaining access to necessary files and directories.
RUN useradd -m -u 1000 wowberg && chown -R wowberg:wowberg /app

# Copy project files
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src

# Install dependencies as root (required for building wheel)
RUN pip install --no-cache-dir .

# Fix permissions for non-root user
RUN chown -R wowberg:wowberg /app

# Switch to non-root user
USER wowberg

EXPOSE 8000
