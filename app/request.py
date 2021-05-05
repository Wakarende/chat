import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify_client_id = None
spotify_client_secret = None


def configure_request(app):
    global spotify_client_id, spotify_client_secret
    spotify_client_id = app.config['SPOTIPY_CLIENT_ID']
    spotify_client_secret = app.config['SPOTIPY_CLIENT_SECRET']


credentials_manager = SpotifyClientCredentials('3acfb5c708b1421888f1d5d74388e27f', '8fa76f281cf540af838095c203ce2c53')
sp = spotipy.Spotify(client_credentials_manager=credentials_manager)


def get_artists():
    return sp.artists()


def get_playlists(query):
    return sp.search(q=query, type='playlist',limit=10)


def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids


def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy,
             instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track
