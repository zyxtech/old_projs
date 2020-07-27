import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db
from app.main.models import *
from app.devices.models import *
from app.demos.models import *

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, c=db.drop_all())


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
        #manager.run()
    #manager.run()
    app.run(host='127.0.0.1', port=9002)
    #app.run(host='0.0.0.0', port=8080)


@app.cli.command()
def deploy():
    db.drop_all()
    db.create_all()