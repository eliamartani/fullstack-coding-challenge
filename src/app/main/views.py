from flask import Blueprint, render_template, request, jsonify
from .service import schedule_translation, check_translation

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
    try:
        from urllib.parse import urlparse
        decoded = urlparse.unquote(text)
    except:
        # Python 2 issue
        # from urlparse import urlparse
        # decoded = urlparse.parse_qs(text)
        decoded = text

    # Translate it
    uid = schedule_translation(decoded)

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
    translated = check_translation(uid)

    if translated and translated.strip():
        # TODO: Save on database
        print(translated)

    # Return JSON structure
    return jsonify({
        'translated': translated
    })


@main.route('/previous', methods=['GET'])
def previous ():
    return jsonify([
        'Teste teste 1',
        'Teste teste 2',
        'Teste teste 3',
        'Teste teste 4',
        'Teste teste 5',
        'Teste teste 6'
    ])
