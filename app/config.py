import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")