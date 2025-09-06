import os
from app import app, socketio

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))

    # Check if running in production (Fly.io sets FLY_APP_NAME)
    is_production = os.getenv("FLY_APP_NAME") is not None

    if is_production:
        # Production mode - this shouldn't typically be reached since
        # Fly.io will use gunicorn, but keeping for safety
        socketio.run(app, host="0.0.0.0", port=port, debug=False)
    else:
        # Development mode
        socketio.run(app, host="0.0.0.0", port=port, debug=True)