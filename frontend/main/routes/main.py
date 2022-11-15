from flask import Flask, session,Blueprint, current_app, render_template, make_response, request, redirect, url_for
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

@app.route('/login', methods=['GET','POST'])
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
            if (response.ok): 

                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])

                #Guardar el token en las cookies y devuelve la pagina 
                response = make_response(redirect(url_for('app.user_main')))
                #response = make_response(user_main(jwt=token)) 
                response.set_cookie("access_token", token)
                response.set_cookie("id", user_id)
                return response
                #return render_template('login.html')
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
        return render_template('main.html', poems=poems["poems"])    
    else:
        return redirect(url_for('app.login'))

@app.route('/profile/user/modify')
def modify_user():
    return render_template('user_modify.html')

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

@app.route('/view/poem/<int:id>', methods=['GET'])
def view_poem(id):
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = {"Content-Type" : "application/json"}
    response = requests.get(api_url, headers=headers)
    poem = json.loads(response.text)
    return render_template('view_poem.html', poem = poem)

# else:
    # return redirect(url_for('app.login'))
@app.route('/logout')
def logout():
    #Crear una request de redirección
    req = make_response(redirect(url_for('app.index')))
    #Borrar cookie
    req.delete_cookie("access_token")
    req.delete_cookie("id")
    return req

@app.route('/poem/create')
def create_poem():
    return render_template('create_poem.html')

@app.route('/poem/<int:id>/delete')
def delete_poem(id):
    if request.cookies.get('accsess_token')
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = {"Content-Type" : "application/json"}
    response = requests.delete(api_url, headers=headers)
    return response