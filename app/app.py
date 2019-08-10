from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

from models import info, Picture


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()

import view
