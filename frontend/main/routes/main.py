from email import header
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
    print(response.status_code)  
    print(response.text)
    poems = json.loads(response.text)
    print(poems)
    return render_template('main.html', poems=poems["poems"])

@app.route('/profile/admin')
def admin_profile():
    return render_template('admin_profile.html')

@app.route('/login')
def login():
    if (request.method == 'POST'):
        #obtener datos del formulario - Esto lo traigo del HTML con los name de los inputs. 
        email = request.form['email']
        password = request.form['password']
        print(email, password)

        if email != None and password != None: 
            #es la url que utilizamos en insomnia
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            #Envio de token
            data = {"email" : email, "password" : password}
            headers = {"Content-Type" : "application/json"}
            
            response = requests.post(api_url, json = data, headers = headers) 
            print("login", response)
            if response.status_code == 200: 

                print(response.status_code)
                print(response.text)

                #obtener el token desde response
                token = json.loads(response.text)
                token = token["access_token"]
                print(token) 

                #Guardar el token en las cookies y devuelve la pagina 
                response = make_response(redirect(url_for('app.user_main')))
                response.set_cookie("access_token", token)

                return response 
                #return render_template('login.html')
            else:
                return render_template('login.html')
        return(render_template('login.html', error = "Usuario o contraseña incorrectos"))
    else:
        return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register_user.html')

@app.route('/home')
def user_main():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems'
        data = { "page": 1, "per_page": 10 }
        headers = { "Content-Type": "application/json" }
        response = requests.get(api_url, json=data, headers=headers) 
        print(response.status_code)  
        print(response.text)
        poems = json.loads(response.text)
        print(poems)
        return render_template('user_main.html', poems=["Poems"])
    else:
        return redirect(url_for('app.login'))

@app.route('/profile/user/modify')
def modify_user():
    return redirect(url_for('app.login'))

@app.route('/profile/user')
def user_profile():
    if request.cookies.get('access_token'):
        api_url = f'{current_app.config["API_URL"]}/poems'
        
        data = { "page": 1, "per_page": 10 }

        headers = { "Content-Type": "application/json" }

        response = requests.get(api_url, json=data, headers=headers) 
        
        return render_template('user_profile.html', poems = ["Poems"])
    else:
        return redirect(url_for('app.login'))