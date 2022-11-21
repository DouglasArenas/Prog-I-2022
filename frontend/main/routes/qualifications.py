from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json

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
            comment = request.form['comment']
            api_url = f'{current_app.config["API_URL"]}/qualifications'
            data = {"score" : score, "comment" : comment, "user_id" : user_id, "poem_id" : id}
            headers = {"Content-Type": "application/json", "Authorization" : f"Bearer {jwt}"}
            response = requests.post(api_url, json=data, headers=headers)
            if response.ok:
                response = json.loads(response.text)
                return redirect(url_for('poems.view_poem', id=response["id"], jwt=jwt))
            return redirect(url_for('poems.view_poem', id=id))
    else:
        return redirect(url_for('app.login'))

# @qualifications.route('/view/qualification/<int:id>', methods=['GET'])
# def view_qualification(id):
#     jwt = request.cookies.get('access_token')
#     if jwt:
#         usuario = request.cookies.get('id')
#         api_url_user = f'{current_app.config["API_URL"]}/user/{usuario}'
#         headers = {"Content-Type":"application/json", "Authorization" : f"Bearer {jwt}"}
#         response = requests.get(api_url_user, headers=headers)
#         user = json.loads(response.text)
#         return render_template('user_profile.html', jwt=jwt, user=user)
#     else:
#         return redirect(url_for('app.login'))