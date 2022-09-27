from flask import Flask, Blueprint, render_template
import requests, json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/profile/admin')
def admin_profile():
    return render_template('admin_profile.html')

@app.route('/auth/login')
def login():
    api_url = "http://127.0.0.1:5000/auth/login"
    data = {"email":"d.arenas@alumno.um.edu.ar", "password":"1234"}
    headers = {"Content-Type":"aplication/json"}
    response = requests.post(api_url, json=data, headers=headers)
    token = json.loads(response.text)
    token = token["access_token"]
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register_user.html')

@app.route('/home')
def user_main():
    return render_template('user_main.html')

@app.route('/profile/user/modify')
def modify_user():
    return render_template('user_modify.html')

@app.route('/profile/user')
def user_profile():
    return render_template('user_profile.html')