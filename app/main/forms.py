from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,IntegerField
from wtforms.validators import Required,Email,EqualTo, InputRequired,Length,NumberRange,URL,Optional
from ..models import User, Playlist,Song,PlaylistSong
from wtforms import ValidationError
from email_validator import validate_email
from wtforms import SelectField

class UpdateProfile(FlaskForm):
  bio = TextAreaField('Tell us about you.',validators = [Required()])
  submit = SubmitField('Submit')

class PlaylistForm(FlaskForm):
  """Form for adding playlists."""
  name = StringField("Playlist Name", validators=[InputRequired()])
  # description = StringField('Playlist Description', validators=[InputRequired()])
  submit = SubmitField('Submit')
 

class SongForm(FlaskForm):
  """Form for adding songs."""
  # Add the necessary code to use this form
  title = StringField("Song Title", validators=[InputRequired()])
  artist = StringField("Artist Name", validators=[InputRequired()])


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
  """Form for adding a song to playlist."""


class SearchSongsForm(FlaskForm):
  """Form for searching music"""
  track = StringField("Search for song or word on a song", validators=[InputRequired()])


class DeleteForm(FlaskForm):
  """Delete form -- this form is intentionally blank."""
