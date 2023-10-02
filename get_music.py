# 1. The model downloads yotuube music
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import eyed3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import requests
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from dotenv import load_dotenv
import os


from config import MUSIC_FOLDER = 'music/'
AUDIO_DOWNLOAD_DIR = "./music/"

def YoutubeAudioDownload(video_url):
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio = True).first()

    try:
        audio_file_path = audio.download(MUSIC_FOLDER)
        print(f"Audio downloaded at {audio_file_path}")
        
        # Convert .mp4 audio file to .mp3
        clip = AudioFileClip(audio_file_path)
        mp3_file_path = os.path.join(MUSIC_FOLDER, f"{video.title.strip().lower()} - {video.author.strip().lower()}.mp3")
        clip.write_audiofile(mp3_file_path)

        # Removing the initial mp4 audio file
        os.remove(audio_file_path)
    except:
        print("Failed to download audio")

    print("audio was downloaded successfully")
    return video

def add_metadata(mp3_file_path, title, author, thumbnail_url):
  ## add metadatas
  audiofile = eyed3.load(mp3_file_path)
  audiofile.tag.title = title
  audiofile.tag.artist = author
  audiofile.tag.save()
  ## add thumbnail
  audio = MP3(mp3_file_path, ID3=ID3)
  response = requests.get(thumbnail_url, stream=True)
  response.raise_for_status()
  image_data = response.content

  try:
      audio.add_tags()
  except error as e:
      pass
      
  audio.tags.add(
      APIC(
          encoding=3,
          mime='image/jpeg',
          type=3, desc=u'Cover',
          data=image_data
      )
  )
  audio.save()

def get_artist_tags(artist_name, song_name='no_song_name', user_tags=None):
  formatted_name = '%20'.join(artist_name.split())
  print('formatted_name', formatted_name)
  url = f"http://musicbrainz.org/ws/2/artist/?query=artist:{formatted_name}&fmt=json"
  response = requests.get(url)
  response.raise_for_status()
  if response.status_code >= 400:
    print('couldnt get tags from musicbrainz')
    return []
  else:
    data = response.json()
    print('data', data)
    if not data['artists']:
      print('couldnt find tags of the artist')
      return []

    tags_raw = (data['artists'][0]['tags'])
    tags = [tag['name'] for tag in tags_raw if tag['count'] > 1]
    if user_tags == None: 
      input_tags = input(f"what tags do you want to add for? {artist_name} {song_name}: ")
      tags += input_tags.split()
    print(tags)
    return tags

def get_chroma_collection(collection_name, get_client=False):
  client = chromadb.PersistentClient(path="./db/")
  default_ef = embedding_functions.DefaultEmbeddingFunction()
  col = client.get_or_create_collection(name=collection_name, embedding_function=default_ef)
  if get_client == True:
     return col, client
  else:
    return col

def get_existing_music_db(path_folder='./music/'):
  """
  this functions takes the music in a folder and puts them in the music database
  """
  files = [file[:-4] for file in os.listdir(path_folder)]
  print('files to process', files)
  for song in files:
    title, author = song.split('-')[:2]
    tags = get_artist_tags(author)
    add_to_database(title, author, tags)
  print('finished adding to database the songs with tags and all') 
  
def add_to_database(title, author, tags):
  col = get_chroma_collection('music')
  processed_name = f"{title} - {author}"
  res = col.get(where={"song_author_names":processed_name})
  if not res['ids']:
    col.add(
      documents=[processed_name + str(tags)],
      metadatas={"song_author_names":processed_name},
      ids=[str(col.count())]
    )
    print(f"added {title} {author} to the database")
  else:
    print('skipped because already in db')

def Download_add_db(video_url, user_tags=None): 
  video = YoutubeAudioDownload(video_url)
  title = video.title.strip().lower()
  author = video.author.strip().lower()
  thumbnail_url = video.thumbnail_url
  file_name = f'{title} - {author}.mp3'
  audio_path = f'{MUSIC_FOLDER}{file_name}'

  add_metadata(audio_path, title, author, thumbnail_url)
  tags = get_artist_tags(author, user_tags)
  add_to_database(title, author, tags)
  print('finished saving song!')
  return file_name[:-4]


