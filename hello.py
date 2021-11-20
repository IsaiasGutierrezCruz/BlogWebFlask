from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p> Your browser is {}</p>'.format(user_agent)

@app.route('/about.html')
def about():
    return '<h1>Im about</>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}! </h1>'.format(name)
