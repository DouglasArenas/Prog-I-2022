from .. import db

class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Integer, nullable=True)
    userId = db.Column(db.Integer)
    poemId = db.Column(db.Integer)

    def __repr__(self):
        return f'<Score: {self.score}, Comment: {self.comment}, User: {self.userId}, Poem {self.poemId}>'

    def to_json(self):
        qualification_json = {
            'id' : self.id,
            'score' : self.score,
            'comment' : self.comment,
            'userId' : self.userId,
            'poemId' : self.poemId
        }
        return qualification_json

    def to_json_short(self):
        qualification_json = {
            'id' : self.id,
            'score' : self.score,
            'userId' : self.userId
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