from .. import db

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Title: {self.title}, UserId: {self.user_id}, Poem: {self.body}, Date {self.date}>'

    def to_json(self):
        poem_json = {
            'id' : self.id,
            'title' : self.title,
            'user_id' : self.user_id,
            'body' : self.body,
            'date' : self.date
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id' : self.id,
            'title' : self.title,
        }
        return poem_json

    @staticmethod
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        user_id = poem_json.get('user_id')
        body = poem_json.get('body')
        date = poem_json.get('date')
        return Poem(id=id, title=title, body=body, date=date)
