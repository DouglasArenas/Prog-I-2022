from .. import db
from . import UserModel

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Integer, nullable=True)
    userId = db.Column(db.Integer, db.ForeingKey('user.id'), nullable=False)
    poemId = db.Column(db.Integer, db.ForeingKey('poem.id'), nullnable=False)
    author = db.relationship('User', back_populates="qualification", uselist=False, single_parents=True)

    def __repr__(self):
        return f'<Score: {self.score}, Comment: {self.comment}, User: {self.userId}, Poem {self.poemId}>'

    def to_json(self):
        self.author = db.session.query(UserModel).get_or_404(self.userId)
        qualification_json = {
            'id' : self.id,
            'score' : self.score,
            'comment' : self.comment,
            'author' : self.author.to_json()
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
        userId = qualification_json.get('userId')
        poemId = qualification_json.get('poemId')
        return Qualification(id=id, score=score, comment=comment, userId=userId, poemId=poemId)
