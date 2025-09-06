FROM python:3.11.1 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt

FROM python:3.11.1-slim
WORKDIR /app

# Copy virtual environment
COPY --from=builder /app/.venv .venv/

# Copy application code
COPY . .

# Make sure the venv binaries are executable
RUN chmod +x .venv/bin/*

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Set the PATH to include venv
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Use gunicorn with eventlet for production
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8080", "--timeout", "120", "--log-level", "info", "run:app"]