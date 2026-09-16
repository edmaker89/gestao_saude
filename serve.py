import os

from waitress import serve

from app.app import create_app


def _env_int(name, default):
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


app = create_app()

serve(
    app,
    host=os.getenv("APP_HOST", "127.0.0.1"),
    port=_env_int("APP_PORT", 5000),
    threads=_env_int("APP_THREADS", 8),
)
