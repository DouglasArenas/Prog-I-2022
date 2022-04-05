from flask_restful import Resource
from flask import request

#Diccionario de prueba
POEMS = {
    1 : {'Título' : 'Elegía' ,'Autor' : 'Miguel'},
    2 : {'Título' : 'Tú me quieres blanca' ,'Autor' : 'Alfonsina'},
    3 : {'Título' : 'Gacela de la terrible presencia' ,'Autor' : 'Federico'},
    4 : {'Título' : 'Me gusta cuando callas' ,'Autor' : 'Pablo'},
    5 : {'Título' : 'Amor constante más allá de la muerte' ,'Autor' : 'Francisco'}
}

class Poem(Resource):
    def get(self, id):
        if int(id) in POEMS:
            return POEMS[int(id)]
        return '', 404

    def delete(self, id):
        if int(id) in POEMS:
            return POEMS[int(id)]
        return '', 404

class Poems(Resource):
    def get(self):
        return POEMS

    def post(self):
        poem = request.get_json()
        id = int(max(POEMS.key())) + 1
        POEMS[id] = poem
        return POEMS[id], 201
