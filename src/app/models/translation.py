from .. import db

class Translation(db.Model):
    __tablename__ = 'translations'
    id = db.Column(db.Integer, primary_key=True)
    from_text = db.Column(db.String(200))
    to_text = db.Column(db.String(200))

    def __init__(self, from_text, to_text):
        self.from_text = from_text
        self.to_text = to_text
