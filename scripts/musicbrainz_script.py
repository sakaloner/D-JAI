### testing musicbrainz
import spotipy
import urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

c_id = os.getenv("SPOTIPY_CLIENT_ID")
c_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
load_dotenv()

client_credentials_manger=SpotifyClientCredentials(client_id=c_id, client_secret=c_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manger)

q = {
    'track':'californication',
    'artist':'red hot chilli peppers',
    'type':'track'
  }
data = urllib.parse.urlencode(q)
res = spotify.search(data)
from pprint import pprint
for x in res['tracks']['items']:
  print(x.keys())
  print('#######################')
  pprint(x['album']['name'])
  pprint(x['artists'][0]['name'])
  pprint(x['artists'][0]['genres'])
  print(x['id'])
  exit()