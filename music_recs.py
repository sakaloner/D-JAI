import random
from pytube import Search
from get_music import get_chroma_collection
from config import MUSIC_FOLDER

def play_songs(player, song_name):
  song_path = f'{MUSIC_FOLDER}{song_name.strip()}.mp3'
  print(song_path)
  command = f"loadfile '{song_path}' + b'\n".encode()
  player.stdin.write(command)
  player.stdin.flush()

def search_play_song(player, song_name):
  col = get_chroma_collection('music')
  res = col.query(
    query_texts=[song_name],
    n_results= 1
  )
  song_name = res['metadatas'][0][0]['song_author_names']
  play_songs(player, song_name)
  return song_name


def get_recs(query_string=None, random_song=False):
  col = get_chroma_collection('music')
  if random_song:
    ids_rand = [str(random.randint(0, (col.count()-1))) for i in range(20)]
    songs = []
    for id_song in ids_rand:
      res = col.get(
        ids=[id_song]
      )
      songs.append(res['metadatas'][0]['song_author_names'])
    return songs
  else:
    res = col.query(
      query_texts=[query_string],
      n_results=5,
    )
    ## recs are a list of songs without .mp3 thing
    songs = ([x['song_author_names'] for x in res['metadatas'][0]])
    return songs

def create_playlist(songs_list, playlist_name):
  # add to the db
  col = get_chroma_collection('playlists')
  res = col.add(
    documents=[playlist_name],
    metadatas={'songs':str(songs_list)},
    ids=[str(col.count())]
  )
  ## add to a file
  songs = [f'{song}.mp3' for song in songs_list]
  with open(f'{MUSIC_FOLDER}{playlist_name}.pls', 'w') as f:
    for s in songs:
      f.write(s+'\n')

def play_random(player):
  songs_list = get_recs(random_song=True)
  songs = [f'{song}.mp3' for song in songs_list]
  with open(f'{MUSIC_FOLDER}random.pls', 'w') as f:
    for s in songs:
      f.write(s+'\n')
  pls_file = f'{MUSIC_FOLDER}random.pls'
  command = f"loadlist '{pls_file}'\n".encode()
  player.stdin.write(command)
  player.stdin.flush()

def search_playlist(playlist_query_name=''):
  col = get_chroma_collection('playlists')
  res = col.query(
     query_texts=[playlist_query_name],
     n_results=10,     
  )
  playlists = res['documents'][0]
  return playlists


def play_playlist(player, playlist_query_name): 
  col = get_chroma_collection('playlists')
  res = col.query(
     query_texts=[playlist_query_name],
     n_results=1,     
  )
  playlist_name = res['documents'][0][0]
  print(playlist_name)
  ## get playlist file
  pls_file = f'{MUSIC_FOLDER}{playlist_name}.pls'
  command = f"loadlist '{pls_file}'\n".encode()
  player.stdin.write(command)
  player.stdin.flush()

def search_youtube(query):
  s = Search(query)
  video_list = []
  for i, x in enumerate(s.results[:5]):
    video_item = f'{i+1}. title:{x.title} author:{x.author}. link:{x.watch_url}'
    video_list.append(video_item)
  return video_list