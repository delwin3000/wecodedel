import os

class Config:
    SECRET_KEY = 'super-secret-key'  # Change this later
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 