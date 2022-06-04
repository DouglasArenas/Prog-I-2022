from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import QualificationModel
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

class Qualification(Resource):

    def get(self, id):
        qualification = db.session.query(QualificationModel).get_or_404(id)
        return qualification.to_json()

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        user_id = get_jwt_identity()
        qualification = db.session.query(QualificationModel).get_or_404(id)
        if "role" in claims:    
            if claims['role'] == "admin" or user_id == qualification.user_id:
                db.session.delete(qualification)
                db.session.commit()
                return '', 204
            else:
                return "Only admins and poets can delete qualifications"
    
    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()
        qualification = db.session.query(QualificationModel).get_or_404(id)
        if user_id == qualification.user_id:
            data = request.get_json().items()
            for key, value in data:
                setattr(qualification, key, value)
            db.session.add(qualification)
            db.session.commit() 
            return qualification.to_json(), 201   
        else:
            return "Only poets can modify qualifications"

class Qualifications(Resource):
    def get(self):
        qualifications = db.session.query(QualificationModel).all()
        return jsonify([qualification.to_json() for qualification in qualifications])
    
    @jwt_required()
    def post(self):
        qualification = QualificationModel.from_json(request.get_json())
        claims = get_jwt()
        if "role" in claims:
            if claims["role"] == "poet":
                db.session.add(qualification)
                db.session.commit()
                return qualification.to_json(), 201
            else:
                return "Only poets can create poems"
        else:
            return "you must be a registered user"