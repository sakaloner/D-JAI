from get_music import get_chroma_collection
import subprocess
import os
import threading

MUSIC_FOLDER = './music/'
def _read_stream(stream):
    while True:
        line = stream.readline()
        if line == b'':  # End of file
            break
        # You may want to do something with 'line' here
        # For now, we'll just print it
        print(line.decode().strip())

def play_songs(player, song_name):
  song_path = f'{MUSIC_FOLDER}{song_name.strip()}.mp3'
  print(song_path)
  #player = subprocess.Popen(['mpg123', './music/ghost town - kanye west.mp3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  #player = subprocess.Popen(['mpg123', '-R'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  player.stdin.write(b'L ' + song_path.encode() + b'\n')
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

def get_recs(query_string):
  col = get_chroma_collection('music')
  res = col.query(
    query_texts=[query_string],
    n_results=5,
  )
  songs = ([x['song_author_names'] for x in res['metadatas'][0]])
  return songs

def create_playlist(songs, playlist_name):
  ## add to the db
  col = get_chroma_collection('playlists')
  res = col.add(
    documents=[playlist_name+'.pls'],
    metadatas={'songs':['i wonder - kanye west.mp3', 'salt & pepper - dope lemon.mp3']},
    ids=[str(col.count())]
  )
  ## add to a file
  return
  songs = [f'{MUSIC_FOLDER}{song}.mp3' for song in songs]
  with open(f'{playlist_name}.pls', 'w') as f:
    for s in songs:
      f.write(s+ '\n')

def play_playlist(player, playlist_query_name): 
  col = get_chroma_collection('playlists')
  res = col.query(
     query_texts=[playlist_query_name],
     n_results=1,     
  )
  playlist_name = res['documents'][0][0]
  print(res['metadatas'])
  ## get playlist file
  

# create_playlist('l', 'babasonicos')
# res = play_playlist('l','babazonicos')
# print(res)
