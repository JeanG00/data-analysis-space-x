from conf import conf
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from flask import Flask
from gevent import monkey
monkey.patch_all()


def create_app(conf_name):
    """ create_app """
    app = Flask(__name__, instance_relative_config=True)
    # CORS config
    CORS(app)
    # env variable start with *FLASK_* will be loaded
    app.config.from_prefixed_env()
    app.config.from_object(conf[conf_name])
    # session/cookie will be available
    app.secret_key = app.config['SECRET_KEY']
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # tell Flask it is behind a Proxy
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    # routes init
    from .routes import init
    init(app)

    # embeded dash init
    from .dash import spacex
    spacex.init(app)

    return app
