import os
from src import create_app

conf_env = os.getenv('FLASK_MODE') or 'default'
app = create_app(conf_env)

if __name__ == '__main__':
    app.run()
