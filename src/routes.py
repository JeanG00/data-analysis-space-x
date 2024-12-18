import traceback
from flask import jsonify, render_template
from werkzeug.exceptions import HTTPException
from markupsafe import Markup
from src.utils import version


def init(app):

    @app.route('/', methods=['GET'])
    def home():
        """Landing page."""
        v = version.get_version()
        welcome = "Hello World!"
        return render_template(
            'index.html',
            version=v,
            content=Markup(welcome))

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
