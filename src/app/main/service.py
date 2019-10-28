import time

from flask import current_app
from unbabel.api import UnbabelApi


def create_model():
    username = current_app.config['UNBABEL_USERNAME']
    api_key = current_app.config['UNBABEL_KEY']
    sandbox = current_app.config['UNBABEL_SANDBOX']

    # Set up account
    return UnbabelApi(username=username, api_key=api_key, sandbox=sandbox)


def schedule_translation(text):
    try:
        # Set up account
        source = current_app.config['UNBABEL_SOURCE']
        target = current_app.config['UNBABEL_TARGET']

        uapi = create_model()

        # Create request
        translation = uapi.post_translations(text=text,
            source_language=source,
            target_language=target)

        return translation.uid
    except:
        print('[unbabel] Error trying to schedule translation')
        return ''


def check_translation(uid):
    try:
        # Set up account
        uapi = create_model()

        # Create request
        translation = uapi.get_translation(uid)

        if (translation.status == 'completed'):
            return translation.translation

        return ''
    except:
        print('[unbabel] Error trying to request data')
        return ''
