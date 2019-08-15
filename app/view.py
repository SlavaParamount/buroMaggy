from app import app, db
from flask import render_template, request, redirect, url_for, flash
from models import info, Picture
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField
from werkzeug import secure_filename
from werkzeug.urls import url_parse
import git
from flask_login import current_user, login_user, logout_user, login_required
from models import Users
from wtforms.validators import DataRequired

class postForm(FlaskForm):
    MsgArea = StringField('Введите сообщение', [
                          validators.Length(min=5, max=139)])

class UploadForm(FlaskForm):
    file = FileField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@app.route('/')
def index():
    posts = info.query.all()
    pics = Picture.query.all()
    print(pics)
    return render_template('index.html', posts=posts, pics=pics)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    allCat = []
    allCat = info.query.all()
    print(allCat)

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        print('file', filename)
        form.file.data.save('static/uploads/' + filename)
        newPic = Picture(link = '../static/uploads/' + filename)
        db.session.add(newPic)
        db.session.commit()
        return redirect(url_for('upload'))
    return render_template('upload.html', form=form, allCat = allCat)

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./app', search_parent_directories=True)
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def post():
    postform = postForm()
    if postform.validate_on_submit():
        k = postform.MsgArea.data
        i = info(message=k)
        db.session.add(i)
        db.session.commit()
    return render_template('post.html', postform=postform)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        deleteID = request.values.get('id')
        info.query.filter(info.id == deleteID).delete()
        db.session.commit()
    posts = info.query.all()
    return render_template('edit.html', posts=posts)
