import os


class Config:
  '''
  General configuration parent class
  '''

  SECRET_KEY= os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://joykirii:kirii@localhost/chat'
  UPLOADED_PHOTOS_DEST ='app/static/photos'

  #Spotify API
  TRACK_API_BASE_URL ="https://api.spotify.com/v1/browse/new-releases?country=US&limit=20&offset=10"
  BASE_URL='https://api.spotify.com'
  OAUTH_TOKEN='BQDTdiN4G_w334Zcwtdi9875XO7xwfWH4XhAMoBz_MpC4ij3NKsYCo1afYHOa8OaorqrySujVPtm42dRYl4ZXhFAO03dqKRm62T5aOAQWDDn1zwpF0WVGMWZs53ohe0AD2CM_XZTaB_kG2hjIZQrmwhImvYt7wrsgI6kMlOZgdhjikyCCzWTA0hI2VPhjPX3QeuQqeAhRMoMPzPt5yIUIQ'


  # Spotify API
  CLIENT_ID= '3acfb5c708b1421888f1d5d74388e27f'
  CLIENT_SECRET= '8fa76f281cf540af838095c203ce2c53'
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
