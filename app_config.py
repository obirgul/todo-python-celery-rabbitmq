import os


class Config(object):
    DATABASE_URI = "mssql+pymssql://analytics:Na%3k8Dii@sqldev.roxy/analyticsdb"
    git_commit_id = os.environ.get("GIT_COMMIT_ID", "")
    VERSION = "0.0.1"
    test = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@db-postgres:5432/flask-deploy'
    CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//'
    CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@broker-rabbitmq//'
    DEBUG = True


class ProductionConfig(Config):
    DATABASE_URI = os.environ.get('DATABASE_URI', "mssql+pymssql://analytics:Na%3k8Dii@sqldev.roxy/analyticsdb")
    VERSION = os.environ.get('VERSION', '1.0')
    test = False
