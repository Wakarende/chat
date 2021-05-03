import os

class Config:
  '''
  General configuration parent class
  '''
  SECRET_KEY= os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://joykirii:kirii@localhost/chat'

class ProdConfig(Config):

  pass


class TestConfig(Config):

  pass

class DevConfig(Config):

  DEBUG=True

config_options = {
  'development': DevConfig,
  'production': ProdConfig,
  'test': TestConfig
}