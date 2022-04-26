from .. import db

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Integer, nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poemId = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)
    author = db.relationship('User', back_populates="qualification", uselist=False, single_parent=True)
    poem = db.relationship('Poem', back_populates="qualification", uselist=False, single_parent=True)

    def __repr__(self):
        return f'<Score: {self.score}, Comment: {self.comment}, User: {self.userId}, Poem {self.poemId}>'

    def to_json(self):
        poem = [poem.to_json() for poem in self.poem]
        user = [user.to_json() for user in self.user]
        qualification_json = {
            'id': self.id,
            'name': (self.name),
            'password': (self.password),
            'role': (self.role),
            'email': (self.email),
            'poem' : poem,
            'user' : user
        }
        return qualification_json

    def to_json_short(self):
        qualification_json = {
            'id' : self.id,
            'score' : self.score
        }
        return qualification_json

    @staticmethod
    def from_json(qualification_json):
        id = qualification_json.get('id')
        score = qualification_json.get('score')
        comment = qualification_json.get('comment')
        poemId = qualification_json.get('poemId')
        return Qualification(id=id, score=score, comment=comment, poemId=poemId)
