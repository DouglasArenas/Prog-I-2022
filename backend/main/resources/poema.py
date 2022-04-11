from flask_restful import Resource
from flask import request

#Diccionario de prueba
POEMS = {
    1 : {'title' : 'Elegía' ,'author' : 'Miguel'},
    2 : {'title' : 'Tú me quieres blanca' ,'author' : 'Alfonsina'},
    3 : {'title' : 'Gacela de la terrible presencia' ,'author' : 'Federico'},
    4 : {'title' : 'Me gusta cuando callas' ,'author' : 'Pablo'},
    5 : {'title' : 'Amor constante más allá de la muerte' ,'author' : 'Francisco'}
}

class Poem(Resource):
    def get(self, id):
        if int(id) in POEMS:
            return POEMS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in POEMS:
            del POEMS[int(id)]
            return '', 204
        return '', 404

class Poems(Resource):
    def get(self):
        return POEMS

    def post(self):
        poem = request.get_json()
        id = int(max(POEMS.keys())) + 1
        POEMS[id] = poem
        return POEMS[id], 201
