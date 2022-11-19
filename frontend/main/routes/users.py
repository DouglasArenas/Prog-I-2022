from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for
import requests
import json


users = Blueprint('users', __name__, url_prefix='/')


@users.route('/home')
def user_main():
    if request.cookies.get('access_token'):
        data = { "page": 1, "per_page": 3 }
        if 'page' in request.args:
            data["page"] = request.args.get('page', '')
        api_url = f'{current_app.config["API_URL"]}/poems' 
        headers = { "Content-Type": "application/json" }
        response = requests.get(api_url, json=data, headers=headers)
        poems = json.loads(response.text)
        pagination = {}
        pagination["pages"] = json.loads(response.text)["pages"]
        pagination["current_page"] = json.loads(response.text)["page"]
        return render_template('main.html', poems=poems["poems"], pagination=pagination)    
    else:
        return redirect(url_for('app.login'))

@users.route('/profile/user')
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

@users.route('/profile/user/modify')
def modify_user():
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'GET':
            user_id = request.cookies.get('id')
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            headers = {'Content-type': 'application/json', 'Authorization': f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)
            user = json.loads(response.text)
            return render_template('user_modify.html', user=user)
        if request.method == 'POST':
            api_url = f'{current_app.config["API_URL"]}/user/{id}'
            data = {"name": request.form['name'], "password": request.form['password']}
            headers = {'Content-type': 'application/json', 'Authorization' : f"Bearer {jwt}"}
            response = requests.put(api_url, json=data, headers=headers)
            return redirect(url_for('users.user_profile', id=id))
    return redirect(url_for('app.login'))

    form = cargar_un_perfil(id)    
    usuario = {
        "nombre": form.nombre.data,
        "apellido": form.apellido.data,
        "telefono": form.telefono.data,
        "mail": form.email.data
    }
    r = requests.put(f'{current_app.config["API_URL"]}/usuario/{id}', headers={"content-type": "application/json"}, json = usuario, auth=BearerAuth(str(request.cookies['access_token'])))

    data = {
        "current_password": form.current_password.data,
        "new_password": form.new_password.data
    }
    if form.new_password.data != '':
        r_password = requests.post(
            f'{current_app.config["API_URL"]}/auth/change-password/{id}',
            headers = {"content-type": "application/json"},
            json = data
        )
        if r_password.status_code == 401:
            flash('La contraseña actual ingresada no es correcta', 'danger')
            return redirect(url_for('cliente.perfil', id = id))
        elif r_password.status_code == 201:
            flash('La contraseña fue actualizada satisfactoriamente', 'success')

    if r.status_code == 201:
        flash('Los datos del perfil fueron actualizados satisfactoriamente', 'info')
        return redirect(url_for('cliente.perfil', id = id))
