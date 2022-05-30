from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel, UserModel
from sqlalchemy import func
from flask_jwt_extended import jwt_required
from main.auth.decorators import admin_required

class User(Resource):
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json_short()
    
    @jwt_required()
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json_short() , 201
    
    @jwt_required()
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class Users(Resource):
    @jwt_required(optional=True)
    def get(self):
        page = 1
        per_page = 10
        users = db.session.query(UserModel)
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Paginate
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "name":
                    users = users.filter(UserModel.name.like('%'+value+'%'))
                # Order
                if key == "sort_by":
                    if key == 'name':
                        users = users.order_by(UserModel.name)
                    if value == "npoems[desc]":
                        users = users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
                    if value == "num_poems":
                        users = users.outerjoin(UserModel.poems).group_by(UserModel.id).order_by(func.count(UserModel.id))
                    if value == "num_qualifications":
                        users = users.outerjoin(UserModel.qualifications).group_by(UserModel.id).order_by(func.count(UserModel.id).desc())
        users = users.paginate(page, per_page, True, 30)
        return jsonify({
            'users' : [user.to_json_short() for user in users.items],
            'total' : users.total,
            'pages' : users.pages,
            'page' : page
        })

    @admin_required
    def post(self):
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json_short(), 201