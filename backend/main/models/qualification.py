from .. import db

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)
    # Relaciones
    author = db.relationship('User', back_populates="qualifications", uselist=False, single_parent=True)
    poem = db.relationship('Poem', back_populates="qualifications", uselist=False, single_parent=True)

    def __repr__(self):
        return f'<Score: {self.score}, Comment: {self.comment}, User: {self.user_id}, Poem {self.poem_id}>'
    # Objeto a JSON
    def to_json(self):
        poem = poem.to_json()
        user = [users.to_json() for users in self.user]
        qualification_json = {
            'id': self.id,
            'name': str(self.name),
            'password': str(self.password),
            'role': str(self.role),
            'email': str(self.email),
            'poem' : poem,
            'user' : user
        }
        return qualification_json

    def to_json_short(self):
        qualification_json = {
            'id' : self.id,
            'score' : self.score,
            'comment' : self.comment,
            'user_id' : self.user_id,
            'poem_id' : self.poem_id
        }
        return qualification_json

    @staticmethod
    # JSON a objeto
    def from_json(qualification_json):
        id = qualification_json.get('id')
        score = qualification_json.get('score')
        comment = qualification_json.get('comment')
        poem_id = qualification_json.get('poem_id')
        user_id = qualification_json.get('user_id')
        return Qualification(id=id, score=score, comment=comment, poem_id=poem_id, user_id=user_id)