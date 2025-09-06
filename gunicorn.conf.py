import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', 8080)}"
backlog = 2048

# Worker processes
workers = 1  # SocketIO requires single worker with eventlet
worker_class = "eventlet"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# Process naming
proc_name = "church-presentation-socketio"

# Server mechanics
preload_app = True
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (handled by Fly.io proxy)
keyfile = None
certfile = None