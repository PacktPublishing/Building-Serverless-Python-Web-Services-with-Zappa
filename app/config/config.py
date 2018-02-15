import os


def get_sqlite_uri(db_name):
    return 'sqlite:////tmp/%s' % db_name


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRON = 'dev'
    SQLALCHEMY_DATABASE_URI = get_sqlite_uri('todo-dev.db')


class ProductionConfig(Config):
    ENVIRON = 'production'
    SQLALCHEMY_DATABASE_URI = get_sqlite_uri('todo-prod.db')


config = {
    'dev': DevelopmentConfig,
    'production': ProductionConfig
}
