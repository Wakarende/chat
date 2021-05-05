from . import main
from flask import render_template,request,redirect,url_for,flash,abort,session
from ..models import User,Playlist
from .forms import UpdateProfile,PlaylistForm
from .. import db,photos
from flask_login import login_required,current_user


@main.route('/')
def index():

  '''
  View root page function that returns the index page and its data
  '''
  title = 'Chat'

  return render_template('index.html',title=title)

#Profile View
@main.route('/user/<uname>')
def profile(uname):
  user = User.query.filter_by(username = uname).first()
  form = PlaylistForm()
  playlists=Playlist.query.filter_by(user_id=current_user._get_current_object().id).all()
  if user is None:
    abort(404)

  if form.validate_on_submit():
    name = form.name.data
    new_playlist = Playlist(name=name, user_id=session['user_id'])
    db.session.add(new_playlist)
    db.session.commit()
    playlists.append(new_playlist)
  
  return render_template("profile/profile.html", user = user, playlists=playlists,form=form )


#Update Profile
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username = uname).first()
  if user is None:
    abort(404)

  form = UpdateProfile()

  if form.validate_on_submit():
    user.bio = form.bio.data

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('.profile',uname=user.username))

  return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username = uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
  return redirect(url_for('main.profile',uname=uname))


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
    # description = form.description.data
    new_playlist = Playlist(name=name,user=user)
    db.session.add(new_playlist)
    db.session.commit()
    return redirect(url_for('main.disp_playlist'))

  return render_template("playlist/new_playlist.html", form=form)

@main.route('/playlists/', methods = ['GET','POST'])
def disp_playlist():
  playlists = Playlist.query.all()
  title='Playlist Display'
  return render_template('playlist/playlists.html', playlists=playlists)

