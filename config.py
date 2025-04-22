import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'super-secret-key'  # Change this later
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
