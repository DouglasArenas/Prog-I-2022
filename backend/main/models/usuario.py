from unicodedata import name
from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    qualification = db.relationship('Qualification', back_populates="author", cascade="all, delete-orphan")
    poem = db.relationship('Poem', back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Name: {self.name}, email : {self.email}, role: {self.role}>'

    def to_json(self):
        qualification = [qualification.to_json() for qualification in self.qualification]
        poem = [poem.to_json() for poem in self.poem]
        poem_json = {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'password' : self.password,
            'role' : self.role,
            'qualification' : qualification,
            'poem' : poem
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id' : self.id,
            'name' : self.name,
        }
        return poem_json

    @staticmethod
    def from_json(user_json):
        id = user_json.get('id')
        name = user_json.get('name')
        email = user_json.get('email')
        password = user_json.get('password')
        role = user_json.get('role')
        return User(id=id, name=name, email=email, password=password, role=role)
