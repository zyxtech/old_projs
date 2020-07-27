# coding: utf-8
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

#app = Flask(__name__)
#app = Flask(__name__, static_folder='/static', static_url_path='/static')
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql://cloudwav_rntix:6459dVVyli@zyxtech.org/cloudwav_test'
##flask sqlalchemy 不支持PYTHON3
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


def make_shell_context():
    return dict(app=app, db=db, User=User)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        admin = User(username=form.name.data, email=form.name.data+'@example.com')
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
         manager.run()