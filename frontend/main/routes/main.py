from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = { "page": 1, "per_page": 10 }
    headers = { "Content-Type": "application/json" }
    response = requests.get(api_url, json=data, headers=headers)
    poems = json.loads(response.text)
    return render_template('main.html', poems=poems["poems"])

@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        if email != None and password != None: 
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            data = {"email" : email, "password" : password}
            headers = {"Content-Type" : "application/json"}
            response = requests.post(api_url, json = data, headers = headers) 
            if (response.ok): 
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])
                response = make_response(redirect(url_for('app.user_main')))
                response.set_cookie("access_token", token)
                response.set_cookie("id", user_id)
                return response
        return(render_template('login.html', error = "Usuario o contraseña incorrectos"))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    req = make_response(redirect(url_for('app.index')))
    req.delete_cookie("access_token")
    req.delete_cookie("id")
    return req

#========================USUARIOS========================#

@app.route('/home')
def user_main():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems' 
        data = { "page": 1, "per_page": 10 }
        headers = { "Content-Type": "application/json" }
        response = requests.get(api_url, json=data, headers=headers)
        poems = json.loads(response.text)
        return render_template('main.html', poems=poems["poems"])    
    else:
        return redirect(url_for('app.login'))

@app.route('/profile/user')
def user_profile():
    jwt = request.cookies.get('access_token')
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/poems'
        data = { "page": 1, "per_page": 10 }
        headers = { "Content-Type": "application/json" }
        response = requests.get(api_url, json=data, headers=headers) 
        poems = json.loads(response.text)
        return render_template('user_profile.html', jwt=jwt, poems=poems ["poems"])
    else:
        return redirect(url_for('app.login'))

@app.route('/profile/user/modify')
def modify_user():
    return render_template('user_modify.html')

#========================POEMAS========================#

@app.route('/profile/user/poemas')
def my_poems():
    jwt = request.cookies.get('access_token')
    if jwt:
        user_id = request.cookies.get('id')
        api_url = f'{current_app.config["API_URL"]}/poems'
        data = {"page":1,"per_page":10}
        headers = {"Content-Type":"application/json", "Authorization" : f"Bearer {jwt}"}
        response = requests.get(api_url, json=data, headers=headers)
        poems = json.loads(response.text)
        return render_template('my_poems.html', poems=poems["poems"])
    else:
        return redirect(url_for('app.login'))

@app.route('/view/poem/<int:id>', methods=['GET'])
def view_poem(id):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = {"Content-Type" : "application/json"}
    response = requests.get(api_url, headers=headers)
    poem = json.loads(response.text)
    return render_template('view_poem.html', poem = poem)

@app.route('/poem/create', methods=['GET','POST'])
def create_poem():
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            user_id = request.cookies.get("id")
            data = {"title": title, "body": body, "user_id": user_id  }
            headers = {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                if response.ok:
                    response = json.loads(response.text)
                    return redirect(url_for('app.view_poem', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('app.create_poem'))
            else:
                return redirect(url_for('app.create_poem'))
        else:
            return render_template('create_poem.html', jwt=jwt)
    else:
        return redirect(url_for('app.login'))

@app.route('/poem/modify/<int:id>', methods=['GET', 'POST'])
def modify_poem(id):
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/poem/{id}'
            headers = {'Content-type': 'application/json', 'Authorization': f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)
            poem = json.loads(response.text)
            return render_template('poem_modify.html', poem=poem)
        if request.method == 'POST':
            api_url = f'{current_app.config["API_URL"]}/poem/{id}'
            data = {"title": request.form['title'], "body": request.form['body']}
            headers = {'Content-type': 'application/json', 'Authorization' : f"Bearer {jwt}"}
            response = requests.put(api_url, json=data, headers=headers)
            return redirect(url_for('app.user_main', id=id))
    return redirect(url_for('app.login'))

@app.route('/poem/<int:id>/delete')
def delete_poem(id):
    jwt = request.cookies.get('access_token')
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/poem/{id}'
        headers = {"Content-Type" : "application/json","Authorization":f"Bearer {jwt}"}
        response = requests.delete(api_url, headers=headers)
        return redirect(url_for('app.user_main'))
    else:
        return redirect(url_for('main.login'))

@app.route('/profile/admin')
def admin_profile():
    return render_template('admin_profile.html')