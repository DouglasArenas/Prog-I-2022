from .. import db
import statistics

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relaciones
    author = db.relationship('User', back_populates="poem", uselist=False, single_parent=True)
    qualifications = db.relationship('Qualification', back_populates="poem", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Title: {self.title}, User Id: {self.user_id}, Poem: {self.body}, Date {self.date}>'

    def score_mean(self):
        qualification_list = []
        if len(self.qualifications) == 0:
            mean = 0
        else:
            for qualification in self.qualifications:
                puntaje = qualification.puntaje
                qualification_list.append(puntaje)
            mean = statistics.mean(qualification_list)

            return mean

    def to_json(self):
        poem_json = {
            'id' : self.id,
            'title' : self.title,
            'body' : self.body,
            'author' : self.author,
            'date' : str(self.date.strftime("%d-%m-%Y")),
            'qualifications' : [qualification.to_json() for qualification in self.qualifications],
            'score_mean' : self.score_mean()
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id' : self.id,
            'title' : self.title,
            'body' : self.body,
            'author' : self.author
        }
        return poem_json

    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        user_id = poem_json.get('user_id')
        body = poem_json.get('body')
        return Poem(id=id, title=title, user_id=user_id, body=body)