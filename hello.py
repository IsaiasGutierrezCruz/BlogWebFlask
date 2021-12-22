from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
Bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    #user_agent = request.headers.get('User-Agent')
    return render_template('index.html', current_time = datetime.utcnow())

@app.route('/about.html')
def about():
    return '<h1>Im about</>'

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500