from flask import Flask, Blueprint, render_template


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def main():
    return render_template('main.html')