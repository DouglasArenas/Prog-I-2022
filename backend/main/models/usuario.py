from unicodedata import name
from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Name: {self.name}, role: {self.role}>'

    def to_json(self):
        poem_json = {
            'id' : self.id,
            'name' : self.name,
            'role' : self.role,
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id' : self.id,
            'name' : self.name,
        }
        return poem_json

    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        name = poem_json.get('name')
        password = poem_json.get('password')
        role = poem_json.get('role')
        return User(id=id, name=name, password=password, role=role)
