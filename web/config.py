import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev"
    SQLALCHEMY_ECHO = True # ustawienie na 'True' przydatne do zadań wykładowych i przy pracy nad sprawozdaniem 2