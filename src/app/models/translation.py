from app import db
from sqlalchemy.inspection import inspect

class Translation(db.Model):
    __tablename__ = 'translations'

    id = db.Column(db.Integer, primary_key=True)
    from_text = db.Column(db.String(200))
    to_text = db.Column(db.String(200))
    uid = db.Column(db.String(20))

    def __init__(self, uid, from_text, to_text):
        self.uid = uid
        self.from_text = from_text
        self.to_text = to_text

    def serialize(self):
        return { c: getattr(self, c) for c in inspect(self).attrs.keys() }
