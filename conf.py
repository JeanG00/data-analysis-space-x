from os import environ


class Conf:
    APP_NAME = environ.get('APP_NAME') or 'da_spacex'
    SECRET_KEY = environ.get('SECRET_KEY')
    JWT_SECRET = environ.get('JWT_SECRET')
    JWT_EXPIRE = 14400  # 4 hours
    SQL_URI = environ.get('SQL_URI') or 'sqlite:///my_sql.db'


class Prod(Conf):
    SOCKET_LOG = False


conf = {
    'dev': Conf,
    'prod': Prod,
    'default': Conf
}
