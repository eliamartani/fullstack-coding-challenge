from flask import current_app
from unbabel.api import UnbabelApi


def unbabel_api_settings():
    username = current_app.config['UNBABEL_USERNAME']
    api_key = current_app.config['UNBABEL_KEY']
    sandbox = current_app.config['UNBABEL_SANDBOX']

    # Set up account
    return UnbabelApi(username=username, api_key=api_key, sandbox=sandbox)


def service_schedule_translation(text):
    try:
        source = current_app.config['UNBABEL_SOURCE']
        target = current_app.config['UNBABEL_TARGET']

        # Set up model
        uapi = unbabel_api_settings()

        # Create request
        translation = uapi.post_translations(text=text,
            source_language=source,
            target_language=target)

        return translation.uid
    except Exception as e:
        print('[unbabel] Error trying to schedule translation')
        print(str(e))

        return ''


def service_check_translation(uid):
    try:
        # Set up model
        uapi = unbabel_api_settings()

        # Create request
        translation = uapi.get_translation(uid)

        return translation.translation
    except Exception as e:
        print('[unbabel] Error trying to request translated data')
        print(str(e))

        return ''
