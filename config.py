import os


class Config:
    """
    General configuration parent class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://joykirii:kirii@localhost/chat'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID','3acfb5c708b1421888f1d5d74388e27f')
    SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET', '8fa76f281cf540af838095c203ce2c53')


class ProdConfig(Config):
    pass


class TestConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}
