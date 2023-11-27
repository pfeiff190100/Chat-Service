class DefaultConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SECRET_KEY = 'verysecretyesyes'

class TestConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

