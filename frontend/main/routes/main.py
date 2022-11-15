from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json


app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = f'{current_app.config["API_URL"]}/poems'
    print("Aca esta la url",api_url)
    data = { "page": 1, "per_page": 10 }
    headers = { "Content-Type": "application/json" }
    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)  
    print(response.text)
    poems = json.loads(response.text)
    print(poems)
    return render_template('main.html', poems=poems["poems"])

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

@app.route('/logout')
def logout():
    req = make_response(redirect(url_for('app.index')))
    req.delete_cookie("access_token")
    req.delete_cookie("id")
    return req

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

@app.route('/profile/user/poemas')
def my_poems():
    jwt = request.cookies.get('access_token')
    if jwt:
        try:
            jwt_decoded = jwt.decode(request.cookies.get['access_token'], algorithms=['HS256'])
            print(jwt_decoded)
        except:
            print('Decoding jwt failed.')
        #Obtenemos usuario
        data_user = {"id": jwt_decoded['id'], "email":jwt_decoded["email"]}

        user_id = request.cookies.get('id')
        api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
        print("Acá esta el id", user_id)
        headers = {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
        response = requests.get(api_url, headers=headers)
        print("El Response user",response)
        user = json.loads(response.text)
        print("Este es el usuario", user)

        #Obtenemos poemas del usuario
        api_url_poems = f'{current_app.config["API_URL"]}/poems'
        data_poems = {"page":1,"per_page":10, "user_id":data_user['id']}
        headers_poems = {"Content-Type":"application/json", "Authorization" : f"Bearer {jwt}"}
        response_poems = requests.get(api_url_poems, json=data_poems, headers=headers_poems)
        response = json.loads(response_poems.text)
        print(response)

        return render_template('mis_poemas.html', jwt=jwt, user=user)
    else:
        return redirect(url_for('app.login'))

    api_url = f'{current_app.config["API_URL"]}/poems'
    # Envio de la pagina y cuantos datos por pagina.
    data = {"page": page, "perpage": perpage, "user_id": id}
    # Obtengo el jwt del logueo e instancio headers y le agrego el jwt.
    headers = get_headers(without_token = True)
    # Creamos el response y le enviamos el data y headers.
    return requests.get(api_url, json = data, headers = headers)

    data = jwt.decode(token, options=jwt_options, algorithms=['HS256'])
    return {'id': data['id'], 'email': data['email']}

    jwt = f.get_jwt()
    if jwt:
        user = auth.load_user(jwt)
        resp = f.get_poems_by_id(user["id"])
        poems = json.loads(resp.text)
        poemsList = poems["poems"]
        return render_template('view_poet_mypoems.html', jwt=jwt, poems = poemsList)
    else:
        return redirect(url_for('main.login'))
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
            print(title)
            print(body)
            user_id = request.cookies.get("id")
            print(user_id)
            data = {"title": title, "body": body, "user_id": user_id  }
            print(data)
            headers = {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                print(response)
                if response.ok:
                    response = json.loads(response.text)
                    return redirect(url_for('app.view_poem', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('app.create_poem'))
            else:
                return redirect(url_for('app.create_poem'))
        else:
            #Mostrar template
            return render_template('create_poem.html', jwt=jwt)
    else:
        return redirect(url_for('app.login'))

@app.route('/poem/<int:id>/delete', methods=['DELETE'])
def delete_poem(id):
    jwt = request.cookies.get('access_token')
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/poem/{id}'
        headers = {"Content-Type" : "application/json","Authorization":f"Bearer {jwt}"}
        response = requests.delete(api_url, headers=headers)
        print("respuesta del delete",response)
        return redirect(url_for('app.user_main'))
    else:
        return redirect(url_for('main.login'))

        if request.cookies.get('access_token'):
            api_url = f'{current_app.config["API_URL"]}/poema/{id}'
            headers = get_headers()
            return requests.delete(api_url, headers=headers)
            f.delete_poema(id=id)
            return redirect(url_for('main.usuario'))
        else:
            return redirect(url_for('main.login'))

@app.route('/profile/admin')
def admin_profile():
    return render_template('admin_profile.html')