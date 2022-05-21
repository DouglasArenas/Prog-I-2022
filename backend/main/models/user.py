from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    # Relaciones
    qualifications = db.relationship('Qualification', back_populates="author", cascade="all, delete-orphan")
    poems = db.relationship('Poem', back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Name: {self.name}, email : {self.email}, role: {self.role}>'
    # Objeto a JSON
    def to_json(self):
        poems = [poem.to_json() for poem in self.poems]
        qualifications = [qualification.to_json_short() for qualification in self.qualifications]
        user_json = {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'password' : self.password,
            'role' : self.role,
            'poems' : poems,
            'qualifications' : qualifications,
        }
        return user_json

    def to_json_short(self):
        user_json = {
            'id' : self.id,
            'name' : self.name,
        }
        return user_json

    @staticmethod
    # JSON a objeto
    def from_json(user_json):
        id = user_json.get('id')
        name = user_json.get('name')
        email = user_json.get('email')
        password = user_json.get('password')
        role = user_json.get('role')
        return User(id=id, name=name, email=email, password=password, role=role)
