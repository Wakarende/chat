import os


class Config:
  '''
  General configuration parent class
  '''

  SECRET_KEY= os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://joykirii:kirii@localhost/chat'
  UPLOADED_PHOTOS_DEST ='app/static/photos'

  #Spotify API
  TRACK_API_BASE_URL ='https://api.spotify.com/v1/browse/new-releases'
  BASE_URL=''
  OAUTH_TOKEN='BQD0reLaZ4rHv53R9TViOt1pezq5Rw8dTPeeQ6Feiofsc8Yqz_boB19ZDH52oFMaRJY7qwYJf_DOHP04gknFcennFx4y3Fxo3MLjoxO1jFvzSiv5brybE8xA_tPiSyjaHYvY7fCkkbt6TitKxVK0DMI1ODwv2M5jBny6DxdRYm7veSRcR9WLlpb9yRCWSsFRFA32Fg'


  # Spotify API
  CLIENT_Id = '3acfb5c708b1421888f1d5d74388e27f'
  CLIENT_SECRET = '8fa76f281cf540af838095c203ce2c53'
  ACCESS_TOKEN_URL = 'https://accounts.spotify.com/api/token'
  AUTH_URL = 'http://accounts.spotify.com/authorize'
  API_VERSION = 'v1'
  API_URL = 'https://api.spotify.com'
  AUTH_METHOD = 'AUTHORIZATION_CODE'


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
