from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PoemModel, UserModel
import datetime
from sqlalchemy import func

class Poem(Resource):
    def get(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        return poem.to_json()

    def delete(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        db.session.delete(poem)
        db.session.commit()
        return '', 204

    #def put(self, id):
        poem = db.session.query(PoemModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(poem,key,value)
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201

class Poems(Resource):
    def get(self):
        poems = db.session.query(PoemModel)
        page = 1
        per_page = 10
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                # Paginate
                if key == "page":
                    page = int(value)
                if key == "per_page":
                    per_page = int(value)
                if key == "title":
                    poems = poems.filter(PoemModel.title.like('%'+value+'%'))
                if key == "user_id":
                    poems = poems.filter(PoemModel.user_id == value)
                if key == "user_name":
                    poems = poems.filter(PoemModel.user_name.has(UserModel.user_name.like('%'+value+'%')))
                if key == "created[gt]":
                    poems = poems.filter(PoemModel.date_time >= datetime.strptime(value, '%d-%m-%Y'))
                if key == "created[lt]":
                    poems = poems.filter(PoemModel.date_time <= datetime.strptime(value, '%d-%m-%Y'))
                # Order
                if key == "sort_by":
                    if value == "author":
                        poems = poems.order_by(PoemModel.author)
                    if value == "author[desc]":
                        poems = poems.order_by(PoemModel.author.desc())
                    if value == "date":
                        poems == poems.order_by(PoemModel.date)
                    if value == "date[desc]":
                        poems = poems.order_by(PoemModel.date.desc())
                    if value == "qualification":
                        poems = poems.outerjoin(PoemModel.qualifications).group_by(PoemModel.id).order_by(func.avg(PoemModel.score))
                    if value == "qualification[desc]":
                        poems = poems.outerjoin(PoemModel.qualifications).group_by(PoemModel.id).order_by(func.avg(PoemModel.score).desc())
        poems = poems.paginate(page, per_page, False, 30)
        return jsonify({
            "poems" : [poem.to_json_short() for poem in poems.items],
            "total" : poems.total,
            "pages" : poems.pages,
            "page" : page
            })

    def post(self):
        poem = PoemModel.from_json(request.get_json())
        db.session.add(poem)
        db.session.commit()
        return poem.to_json(), 201