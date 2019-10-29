import sys

from flask import Blueprint, render_template, request, jsonify
from .service import service_schedule_translation, service_check_translation
from .db import db_store_translation, db_store_schedule, db_previous_translations
from ..models import Translation

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/schedule', methods=['GET'])
def schedule():
    # Read from rquest
    text = request.args.get('value')

    # Deny empty values
    if not text or not text.strip():
        return jsonify({ 'message': 'Empty value to translate' }), 422

    # Decode text
    PYTHON_VERSION = sys.version_info[0]

    if PYTHON_VERSION == 3:
        from urllib.parse import urlparse

        decoded = urlparse.unquote(text)
    else:
        from urlparse import urlparse

        decoded = urlparse.parse_qs(text)

    # Translate it
    uid = service_schedule_translation(decoded)

    # Store record in database
    translation = Translation(uid, decoded, None)

    db_store_schedule(translation)

    # Return JSON structure
    return jsonify({
        'uid': uid
    })


@main.route('/check', methods=['GET'])
def translate():
    # Read from rquest
    uid = request.args.get('value')

    # Deny empty values
    if not uid or not uid.strip():
        return jsonify({ 'message': 'Empty value to translate' }), 422

    # Translate it
    translated = service_check_translation(uid)

    if translated and translated.strip():

        db_store_translation(uid, translated)

    # Return JSON structure
    return jsonify({
        'translated': translated
    })


@main.route('/previous', methods=['GET'])
def previous ():
    list = db_previous_translations()

    return list
