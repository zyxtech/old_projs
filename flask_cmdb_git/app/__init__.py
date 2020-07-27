# encoding: utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_login import LoginManager
# from celery import Celery
from config import BaseConfig
from flask_swagger import swagger
from datetime import timedelta


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

app = Flask(__name__)
login_manager = LoginManager()
# celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL)
swag = swagger(app)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hard to guess string'
    app.config['SECRET_KEY'] = "\x13\x0e\xdalE\x02x\x82=\x8c\x1b\xb9~\xf1#\xe8k\xe1>\xeb\xd7s\xed\x95"
    app.permanent_session_lifetime = timedelta(minutes=120)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://root:xHw123456!@10.129.0.253/xh_cmdb_test'

    #app.config['SQLALCHEMY_DATABASE_URI'] = \
    #    'mysql://cloudwav_rntix:6459dVVyli@zyxtech.org/cloudwav_test'

    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'mysql://root:123456@172.18.19.75/xh_cmdb'

        ##flask sqlalchemy 不支持PYTHON3
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .devices import devices as devices_blueprint
    app.register_blueprint(devices_blueprint)

    from .demos import demos as demos_blusprint
    app.register_blueprint(demos_blusprint)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'main.login'
    login_manager.login_message = u""
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from app.main.models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

