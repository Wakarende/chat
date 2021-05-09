from . import main
from flask import render_template,request,redirect,url_for,flash,abort,session
from ..models import User,Playlist,Song,PlaylistSong
from .forms import UpdateProfile,PlaylistForm,SongForm,NewSongForPlaylistForm
from .. import db,photos
from flask_login import login_required,current_user
from .helpers import first
from spotify import spotify

sp = spotify.Spotify('3acfb5c708b1421888f1d5d74388e27f', '8fa76f281cf540af838095c203ce2c53')


@main.route('/')
def index():
  '''
  View root page function that returns the index page and its data
  '''
  
  # new_tracks= get_tracks()
  title = 'Chart'
  return render_template('index.html', title='Chart')



# Profile View
@main.route('/user/<uname>')
def profile(uname):
  user = User.query.filter_by(username=uname).first()
  form = PlaylistForm()
  playlists = Playlist.query.filter_by(user_id=current_user._get_current_object().id).all()
  if user is None:
    abort(404)

  if form.validate_on_submit():
    name = form.name.data
    new_playlist = Playlist(name=name, user_id=session['user_id'])
    db.session.add(new_playlist)
    db.session.commit()
    playlists.append(new_playlist)

  return render_template("profile/profile.html", user=user, playlists=playlists, form=form)


# Update Profile
@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username=uname).first()
  if user is None:
    abort(404)

  form = UpdateProfile()

  if form.validate_on_submit():
    user.bio = form.bio.data

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('.profile', uname=user.username))

  return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username=uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
  return redirect(url_for('main.profile', uname=uname))


@main.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
  """Show detail on specific playlist."""

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
  playlist = Playlist.query.get_or_404(playlist_id)
    # songs = PlaylistSong.query.filter_by(playlist_id=playlist_id)

    # for b in songs:
    #   print('testing',b)

  return render_template("playlist/playlist.html", playlist=playlist)


@main.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
  """Handle add-playlist form:
  - if form not filled out or invalid: show form
  - if valid: add playlist to SQLA and redirect to list-of-playlists
  """
  form = PlaylistForm()

  if form.validate_on_submit():
    name = form.name.data
    user = current_user
       
    new_playlist = Playlist(name=name, user=user)
    db.session.add(new_playlist)
    db.session.commit()
    return redirect(url_for('main.disp_playlist'))

  return render_template("playlist/new_playlist.html", form=form)

# Songs 
@main.route("/songs")
def show_all_songs():
  """Show list of songs."""

  songs = Song.query.all()
  return render_template("song/songs.html", songs=songs)


@main.route("/songs/<int:song_id>")
def show_song(song_id):
  """return a specific song"""

  song = Song.query.get_or_404(song_id)
  playlists = song.play_song


  return render_template("song/song.html", song=song, playlists=playlists)


@main.route("/songs/add", methods=["GET", "POST"])
def add_song():
  """Handle add-song form:

  - if form not filled out or invalid: show form
  - if valid: add playlist to SQLA and redirect to list-of-songs
  """
  form = SongForm()
  songs = Song.query.all()

  if form.validate_on_submit():
    title = request.form['title']
    artist = request.form['artist']
    new_song = Song(title=title,artist=artist)
    db.session.add(new_song)
    db.session.commit()
    return redirect("/songs")

  return render_template("song/new_song.html", form=form)



@main.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
  """Add a playlist and redirect to list."""
    
  playlist = Playlist.query.get_or_404(playlist_id)
  form = NewSongForPlaylistForm()

  # Restrict form to songs not already on this playlist

  curr_on_playlist = [s.id for s in playlist.songs]
  form.song.choices = (db.session.query(Song.id, Song.title).filter(Song.id.notin_(curr_on_playlist)).all())

  if form.validate_on_submit():    
    song = Song.query.get(form.song.data)
    playlist.songs.append(song)
    db.session.commit()

    return redirect(f"/playlists/{playlist_id}")

  return render_template("song/add_song_to_playlist.html", playlist=playlist, form=form)

# @main.route('/search/<song_name>')
# def search()

@main.route('/playlists/', methods=['GET', 'POST'])
def disp_playlist():
  playlists = Playlist.query.all()
  title = 'Playlist Display'
  return render_template('playlist/playlists.html', playlists=playlists)


@main.route('/playlists/<int:playlist_id>/search', methods=["GET", "POST"])
def show_form(playlist_id):
  """Show form that searches new form, and show results"""
  playlist = Playlist.query.get(playlist_id)
  play_id = playlist_id
  form = SearchSongsForm()
  resultsSong = []
  checkbox_form = request.form

  list_of_songs_spotify_id_on_playlist = []
  for song in playlist.songs:
    list_of_songs_spotify_id_on_playlist.append(song.spotify_id)
  songs_on_playlist_set = set(list_of_songs_spotify_id_on_playlist)

  if form.validate_on_submit() and checkbox_form['form'] == 'search_songs':
    track_data = form.track.data
    api_call_track = sp.search(track_data, 'track')

    # get search results, don't inclue songs that are on playlist already
    for item in api_call_track['tracks']['items']:
      if item['id'] not in songs_on_playlist_set:
        images = [image['url'] for image in item['album']['images']]
        artists = [artist['name'] for artist in item['artists']]
        urls = item['album']['external_urls']['spotify']
        resultsSong.append({
          'title': item['name'],
          'spotify_id': item['id'],
          'album_name': item['album']['name'],
          'album_image': first(images, ''),
          'artists': ", ".join(artists),
          'url': urls
        })

    # search results checkbox form
  if 'form' in checkbox_form and checkbox_form['form'] == 'pick_songs':
    list_of_picked_songs = checkbox_form.getlist('track')
    # map each item in list of picked songs
    jsonvalues = [json.loads(item) for item in list_of_picked_songs]

    for item in jsonvalues:
      title = item['title']
      spotify_id = item['spotify_id']
      album_name = item['album_name']
      album_image = item['album_image']
      artists = item['artists']
            # print(title)
      new_songs = Song(title=title, spotify_id=spotify_id, album_name=album_name, album_image=album_image,
                             artists=artists)
      db.session.add(new_songs)
      db.session.commit()
            # add new song to its playlist
      playlist_song = PlaylistSong(song_id=new_songs.id, playlist_id=playlist_id)
      db.session.add(playlist_song)
      db.session.commit()

    return redirect(f'/playlists/{playlist_id}')

  def serialize(obj):
    return json.dumps(obj)

  return render_template(
    'song/search_new_songs.html', playlist=playlist, form=form, resultsSong=resultsSong, serialize=serialize
  )


@main.route("/playlists/<int:playlist_id>/update", methods=["GET", "POST"])
def update_playlist(playlist_id):
  """Show update form and process it."""
  playlist = Playlist.query.get(playlist_id)
  if "user_id" not in session or playlist.user_id != session['user_id']:
    flash("You must be logged in to view!")
    return redirect("/login")
  form = PlaylistForm(obj=playlist)
  if form.validate_on_submit():
    playlist.name = form.name.data
    db.session.commit()
    return redirect(f"/users/profile/{session['user_id']}")
  return render_template("/playlist/edit.html", form=form, playlist=playlist)


@main.route("/playlists/<int:playlist_id>/delete", methods=["POST"])
def delete_playlist(playlist_id):
  """Delete playlist."""

  playlist = Playlist.query.get(playlist_id)
  if "user_id" not in session or playlist.user_id != session['user_id']:
    raise Unauthorized()

  form = DeleteForm()

  if form.validate_on_submit():
    db.session.delete(playlist)
    db.session.commit()

  return redirect(f"/users/profile/{session['user_id']}")
