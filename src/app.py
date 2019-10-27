import os

from flask import Flask
from app import create_app

app = create_app(os.getenv('APP_ENV', 'default'))

if __name__ == '__main__':
    app.run()
