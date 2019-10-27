from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    translations = [
        'Teste teste 1',
        'Teste teste 2',
        'Teste teste 3',
        'Teste teste 4',
        'Teste teste 5',
        'Teste teste 6'
    ]

    return render_template('main/index.html', translations=translations)
