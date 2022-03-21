from flask_restful import Resource
from flask import request

CALIFICACIONES = {
    1 : {'calification' : 5},
    2 : {'calification' : 4},
    3 : {'calification' : 2}
}

class Qualification(Resource):
    def get(self, id):
        if int(id) in CALIFICACIONES:
            return CALIFICACIONES[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in CALIFICACIONES:
            del CALIFICACIONES[int(id)]
            return '', 204
        return '', 404

class Qualifications(Resource):
    def get(self):
        return CALIFICACIONES

    def post(self):
        qualification = request.get_json()
        id = int(max(CALIFICACIONES.key())) + 1
        CALIFICACIONES[id] = qualification
        return CALIFICACIONES[id], 201
