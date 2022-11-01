from email import header
from flask import Flask, Blueprint, current_app, render_template, make_response, request
import requests, json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = f'{current_app.config["API_URL"]}'
    cookie = request.cookies.get("access_token")
    data = {"page" : 1, "per_page" : 10}
    headers = {f"Content-Type" : "application/json", "Authorization" : "Bearer {cookie}"}
    response = request
    return render_template('main.html')

@app.route('/profile/admin')
def admin_profile():
    return render_template('admin_profile.html')

@app.route('/login')
def login():
    api_url = f'{current_app.config["API_URL"]}/auth/login'
    data = {"email":"douglasarenas71@gmail.com", "password":"1234"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=data, headers=headers)
    print(response.status_code)
    print(response.text)
    token = json.loads(response.text)
    token = token["access_token"]
    print(token)
    resp = make_response(render_template("login.html"))
    resp.set_cookie("access_token", token)
    return resp

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