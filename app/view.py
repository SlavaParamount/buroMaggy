from app import app, db
from flask import render_template, request, redirect, url_for
from models import info, Picture
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
from flask_wtf.file import FileField
from werkzeug import secure_filename


class postForm(FlaskForm):
    MsgArea = StringField('Введите сообщение', [
                          validators.Length(min=5, max=139)])

class UploadForm(FlaskForm):
    file = FileField()


@app.route('/')
def index():
    posts = info.query.all()
    pics = Picture.query.all()
    print(pics)
    return render_template('index.html', posts=posts, pics=pics)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('static/uploads/' + filename)
        newPic = Picture(link = '../static/uploads/' + filename)
        db.session.add(newPic)
        db.session.commit()
        return redirect(url_for('upload'))
    return render_template('upload.html', form=form)


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
