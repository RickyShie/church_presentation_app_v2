FROM python:3.11.1 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt

FROM python:3.11.1-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .

# Use gunicorn with eventlet for production
CMD ["/app/.venv/bin/gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8080", "run:app"]