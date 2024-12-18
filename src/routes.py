import traceback
from flask import jsonify
from werkzeug.exceptions import HTTPException
from src.controllers import *


def init(app):
    @app.route('/heartbeat')
    def heartbeat():
        return jsonify(code=0, message='healthy'), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify(
                code=f"40{e.code}", message=f"{e.name}: {e.description}"), 200
        stack = traceback.extract_stack().format()
        print('{:>^80}'.format(' EXCEPTION '))
        print(stack)
        return jsonify(code=-1, message=f"Unexcepted: {e.args[0]}"), 200

    # blueprints regist
    app.register_blueprint(home.bp)
