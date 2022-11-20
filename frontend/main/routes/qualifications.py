from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json


def add_mark(user_id, poem_id, score, comment):
    jwt = request.cookies.get('access_token')
    api_url = f'{current_app.config["API_URL"]}/qualifications'
    data = {"user_id": user_id, "poem_id": poem_id, "score": score, "comment": comment}
    headers = {"Content-Type": "application/json", "Authorization" : f"Bearer {jwt}"}
    return requests.post(api_url, json = data, headers = headers)


qualifications = Blueprint('qualifications', __name__, url_prefix='/')

@qualifications.route('/poem/qualification/<id>', methods=['GET', 'POST'])
def qualification_add(id):
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/poem/{id}'
            headers = {"Content-Type" : "application/json"}
            response = requests.get(api_url, headers=headers)
            poem = json.loads(response.text)
            print("ESTE ES EL POEMA",poem)
            return render_template('qualification_create.html', poem=poem)

        if request.method == 'POST':
            user_id = request.cookies.get('id')
            score = request.form['score']
            commentary = request.form['comment']
            headers = {"Content-Type": "application/json", "Authorization" : f"Bearer {jwt}"}
            response = add_mark(user_id=user_id, poem_id=id, score=score, comment=commentary) ### ACA ESTA EL ERROR
            if response.ok:
                response = json.loads(response.text)
                return redirect(url_for('qualifications.view_qualification', id=response["id"], jwt=jwt))
            print("ESTE ES EL RESPONSE",response)
            return redirect(url_for('poems.view_poem', id=id))
    else:
        return redirect(url_for('app.login'))

@qualifications.route('/view/qualification/<int:id>', methods=['GET'])
def view_qualification(id):
    jwt = request.cookies.get('access_token')
    if jwt:
        usuario = request.cookies.get('id')
        api_url_user = f'{current_app.config["API_URL"]}/user/{usuario}'
        headers = {"Content-Type":"application/json", "Authorization" : f"Bearer {jwt}"}
        response = requests.get(api_url_user, headers=headers)
        user = json.loads(response.text)
        return render_template('user_profile.html', jwt=jwt, user=user)
    else:
        return redirect(url_for('app.login'))