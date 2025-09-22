# DNS By Eye Standalone Dockerfile
FROM python:3.11.9-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install system dependencies with security updates
RUN apt-get update && apt-get install -y \
    graphviz \
    curl \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files with proper ownership
COPY --chown=appuser:appuser app/ app/
COPY --chown=appuser:appuser config.py ./
COPY --chown=appuser:appuser *.py ./

# Create directories for generated files with proper ownership
RUN mkdir -p app/static/generated \
    && chown -R appuser:appuser app/static/generated

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application with gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=2", "--timeout=120", "app.main:app"]
