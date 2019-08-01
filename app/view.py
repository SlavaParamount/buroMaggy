from app import app, db
from flask import render_template, request
from models import info
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators


class postForm(FlaskForm):
    MsgArea = StringField('Введите сообщение', [
                          validators.Length(min=5, max=139)])


@app.route('/')
def index():
    posts = info.query.all()
    return render_template('index.html', posts=posts)


@app.route('/addpost', methods=['GET', 'POST'])
def post():
    postform = postForm()
    if postform.validate_on_submit():
        k = postform.MsgArea.data
        i = info(message=k)
        db.session.add(i)
        db.session.commit()
    return render_template('post.html', postform=postform)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        deleteID = request.values.get('id')
        info.query.filter(info.id == deleteID).delete()
        db.session.commit()
    posts = info.query.all()
    return render_template('edit.html', posts=posts)
