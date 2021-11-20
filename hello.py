from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    #user_agent = request.headers.get('User-Agent')
    return render_template('index.html')

@app.route('/about.html')
def about():
    return '<h1>Im about</>'

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)