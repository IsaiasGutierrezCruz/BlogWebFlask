from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment # manage dates 
from datetime import datetime # get dates 
# build web forms 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'
Bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    #user_agent = request.headers.get('User-Agent') #example of a request
    form = Form1()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time = datetime.utcnow(), form = form, name = session.get('name'))

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