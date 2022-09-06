from flask import Flask, Blueprint, render_template


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def main():
    return render_template('main.html')

@app.route('/profile/admin')
def profile():
    return render_template('admin_profile.html')

@app.route('/login')
def profile():
    return render_template('login.html')

@app.route('/register')
def profile():
    return render_template('register_user.html')

@app.route('/main')
def profile():
    return render_template('user_main.html')

@app.route('/profile/user/modify')
def profile():
    return render_template('user_modify.html')

@app.route('/profile/user')
def profile():
    return render_template('user_profile.html')