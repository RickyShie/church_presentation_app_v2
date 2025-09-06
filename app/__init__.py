from flask import Flask
from config import Config
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure SocketIO for Fly.io deployment
cors_origins = os.getenv('CORS_ORIGINS', '*')
if cors_origins == '*':
    cors_allowed_origins = '*'
else:
    cors_allowed_origins = cors_origins.split(',')

socketio = SocketIO(
    app,
    async_mode="eventlet",
    cors_allowed_origins=cors_allowed_origins,
    # Fly.io specific optimizations
    ping_timeout=60,
    ping_interval=25,
    # Enable WebSocket transport primarily, fallback to polling
    transports=['websocket', 'polling'],
    # Ensure proper headers for Fly.io proxy
    engineio_logger=False,
    socketio_logger=False
)

from app import routes, models
from app.models import Bible

@app.shell_context_processor
def make_shell_context():
    return { "db": db, "Bible": Bible }