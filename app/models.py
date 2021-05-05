from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))



class User(UserMixin,db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer,primary_key = True)
  username = db.Column(db.String(255))
  pass_secure = db.Column(db.String(255))
  email = db.Column(db.String(255),unique = True,index = True)
  bio = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String())

  @property
  def password(self):
    raise AttributeError('You cannot read the password attribute')

  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)


  def verify_password(self,password):
    return check_password_hash(self.pass_secure,password)


  def __repr__(self):
    return f'User {self.username}'


class Playlist(db.Model):
  """Playlist."""
  __tablename__= "playlists"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False)
  play_s = db.relationship('PlaylistSong', backref='Playlist')
  song = db.relationship('Song', secondary='playlist_song', backref='playlists')
   
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

  user =   db.relationship("User",  backref="playlists")


class Song(db.Model):
  """Song."""
  __tablename__= "songs"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30), nullable=False)
  artist = db.Column(db.String(20), nullable=False)
  play_song = db.relationship(
    'Playlist',
    secondary="playlist_song",
    # cascade="all,delete",
    backref="songs",
  )

   
class PlaylistSong(db.Model):
  """Mapping of a playlist to a song."""
  __tablename__ = "playlist_song"
  playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
  song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)


