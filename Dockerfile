FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 wowberg && chown -R wowberg:wowberg /app

# Install dependencies from the project metadata (as root, required for system packages).
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
RUN pip install --no-cache-dir .

# Switch to non-root user
USER wowberg

EXPOSE 8000
