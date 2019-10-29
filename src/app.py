import os

from flask import Flask

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db

app = create_app(os.getenv('APP_ENV', 'default'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    print('[app] Recreate database')

    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
