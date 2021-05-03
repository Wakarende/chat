from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
  app=Flask(__name__)

  # Creating the app configurations
  app.config.from_object(config_options[config_name])

  #Intitializing Flask Extensions
  bootstrap.init_app(app)
  db.init_app(app)

   # Regestering the main blueprint
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  # Regestering the auth bluprint
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/auth')

  # configure_uploads(app)

  return app