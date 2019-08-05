from app import db


class info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200))

    def __repr__(self):
        return '<Msg: {}>'.format(self.message)

class Picture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	link = db.Column(db.String(100))