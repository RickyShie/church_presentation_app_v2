import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    print(f"SECRET_KEY: {SECRET_KEY}")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(basedir, 'db.sqlite3')}"