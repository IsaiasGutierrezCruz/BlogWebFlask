from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment # manage dates 
from datetime import datetime # get dates 
# build web forms 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# database
from flask_sqlalchemy import SQLAlchemy
import psycopg2
# migrations
from flask_migrate import Migrate
# email 
from flask_mail import Mail, Message
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'
Bootstrap = Bootstrap(app)
moment = Moment(app)
# database
app.config['SQLALCHEMY_DATABASE_URI'] =\
    "postgresql://root:qwerty@localhost/dbflask2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# migration
migrate = Migrate(app, db)
# email
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
mail = Mail(app)
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')



@app.route('/', methods = ['GET', 'POST'])
def index():
    form = Form1()
    # validate the form's data
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            # create the user if he does not exist and assign a role to him/her
            user_role = Role.query.filter_by(name='User').first()
            user = User(username = form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # send email
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New user', 'mail/new_user', user = user)
            flash('You has been registered')
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time = datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known', False))

@app.route('/about.html')
def about():
    return '<h1>Im about</>'

@app.route('/user/<user>')
def user(user):
    return render_template('user.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500

# ----- forms  --------------------
class Form1(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# ----- construct entities -----
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username


# ----------- create and register of the shell context processor ---------
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# --------------- Emails --------------------
def send_email(to, subject, template, **kwards):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwards)
    msg.html = render_template(template + '.html', **kwards)
    mail.send(msg)
