from flask import Flask, render_template
from foogg import auth, api
from foogg.extensions import db, jwt, socketio
from .helpers import loadconf


def create_app(config=None, testing=False, cli=False):
    '''Application factory, used to create application
    '''
    app = Flask('FOOGG',
                template_folder='./templates',
                static_folder='./static')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


def configure_app(app, testing=False):
    '''set configuration for application
    '''
    # default configuration
    env_conf = loadconf()
    app.config.from_object(env_conf)

    if testing is True:
        # override with testing config
        app.config.from_object('foogg.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar(
            'FOOGG_ENV', silent=True)


def configure_extensions(app, cli):
    '''configure flask extensions
    '''
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    # Configue cors for localhost
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin',
                             '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,OPTIONS,DELETE,PATCH,POST,DELETE')
        return response


def register_blueprints(app):
    '''register all blueprints for application
    '''
    # Register socketio events
    from . import events

    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
