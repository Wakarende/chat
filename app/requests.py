import json,urllib.request
from .models import Tracks

import requests



client_id = None
client_secret = None
track_url = None
base_url=None
token=None
def configure_request(app):
  global client_id,client_secret,track_url,base_url,token
  client_id = app.config['CLIENT_ID']
  client_secret = app.config['CLIENT_SECRET']
  track_url=app.config['TRACK_API_BASE_URL']
  base_url=app.config['BASE_URL']
  token=app.config['OAUTH_TOKEN']

def get_tracks():
  '''
  Function that gets the json responce to our url request
  '''
  track_url ="https://api.spotify.com/v1/browse/new-releases?country=US&limit=20&offset=10?".format(token)

  with urllib.request.urlopen(track_url) as url:
    get_tracks_data = url.read()
    get_tracks_response = json.loads(get_tracks_data)

    track_results = None

    if get_tracks_response['data']:
      track_results_list = get_tracks_response['data']
      track_results = process_results(track_results_list)


  return track_results

def process_track_results(track_list):
  
  track_results = []
  for track_item in track_list:
    id = track_item.get('id')
    name = track_item.get('name')
    image = track_item.get('image')
    type = track_item.get('type')
    release_date=track_item.get('release_date')

  return track_results

