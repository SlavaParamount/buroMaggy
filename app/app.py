from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from models import info, Picture


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()

import view
