from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db_init import init_db

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Initialiser la base de données
with app.app_context():
    init_db()
    db.create_all()

from routes import *

if __name__ == '__main__':
    app.run(debug=True)