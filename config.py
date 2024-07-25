import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql://YOUR_USERNAME:YOUR_PASSWORD@localhost/car_rental'
    SQLALCHEMY_TRACK_MODIFICATIONS = False