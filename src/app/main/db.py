from app import db
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from ..models import Translation


def db_previous_translations():
    try:
        translations = Translation.query.filter(Translation.to_text.isnot(None)).order_by(Translation.id.desc()).limit(5).all()

        return jsonify([e.serialize() for e in translations])
    except Exception as e:
        print('[db] Error trying to retrieve data from database')
        print(str(e))

        return {}


def db_store_schedule(translation):
    try:
        db.session.add(translation)
        db.session.commit()
    except Exception as e:
        print('[db] Error trying to save data in database')
        print(str(e))


def db_store_translation(uid, to_text):
    try:
        translation = Translation.query.filter_by(uid=uid).first()
        translation.to_text = to_text

        db.session.commit()
    except Exception as e:
        print('[db] Error trying to update data from database')
        print(str(e))
