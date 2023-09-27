model_functions = [
    ## Reminder functions
    {
        "name": "save_youtube_mp3",
        "description": "download the mp3 from a youtube video and add it to the database with tags",
        "parameters": {
            "type": "object",
            "properties": {
                "url":{
                    "type": "string",
                    "description": "the url of the music video"
                },
                "tags": {
                    "type": "string",
                    "description": "the tags to save the music with eg: 'rock jazz upbeat' add tags you find appropiate for the music"
                }
            },
            "required": ["url","tags"],
        },
    },
    {
        "name": "create_playlist",
        "description": "from the user request output a set of music related tags and a playlistname",
        "parameters": {
            "type": "object",
            "properties": {
                "tags": {
                    "type": "string",
                    "description": "the music related tags to find a music recommendation ex:'hip hop chill jazz new funk'"
                },
                "playlist_name": {
                    "type":"string",
                    "description": "the name of the playlist"
                }
            },
            "required": ["tags", "playlist_name"],
        },
    },
    {
        "name": "search_play_song",
        "description": "search a song for the user to send to the media player",
        "parameters": {
            "type": "object",
            "properties": {
                "song_name": {
                    "type": "string",
                    "description": "the aproximate name of the song"
                },
            },
            "required": ["song_name"],
        },
    },
    {
        "name": "pause_or_play_song",
        "description": "send the command to the media player to pause the song or resume it playing",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ['pause','unpause'],
                    "description": "operation to perform"
                },
                },
            "required": [],
        },
    },
    {
        "name": "skip_song",
        "description": "send the command to the media player to skip the current song",
        "parameters": {
            "type": "object",
            "properties": {
                },
            "required": [],
        },
    },
]
import logging
logging.basicConfig(
  filename='functions.log',
  filemode='w',
  format='%(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)


from get_music import Download_add_db
from music_recs import get_recs, create_playlist, search_play_song
## this should return the function response and system prompt joined already
def function_caller(chatbot, f_name, f_args):
    if f_name == 'save_youtube_mp3':
        print(f_name, f_args)
        song_name = Download_add_db(f_args['url'], f_args['tags'])
        return f"Downloaded {song_name} sucessfully"
    elif f_name == 'create_playlist':
        print(f_name, f_args)
        tags = f_args["tags"]
        playlist_name = f_args["playlist_name"]
        songs = get_recs(f_args['tags'])
        create_playlist(songs, playlist_name)
        return f'recommend these songs and only these to the user: {songs} and tell them the playlist with name {playlist_name} was succesfully created'
    elif f_name == "search_play_song":
        print(f_name, f_args)
        song_name = f_args['song_name']
        logging.info(f_args)
        search_play_song(chatbot.player, song_name)
        return f'the song {song_name} is now playing. tell the user the song is playing'
    elif f_name ==  "pause_or_play_song":
        print(f_name, f_args)
        operation = f_args['operation']
        print('operation', operation)
        if operation == 'unpause':
            chatbot.player.stdin.write(b't\n')
            chatbot.player.stdin.flush()
        else:
            chatbot.player.stdin.write(b'p\n')
            chatbot.player.stdin.flush()
        return f'{operation} song'
    elif f_name == "skip_song":
        ## do something if the state is playlist or random.
        if chatbot.playlist_mode:
            chatbot.player.stdin.write(b'pt_step 1\n')
            chatbot.player.stdin.flush()
        else:
            # play_random()
        return f'skipped song'

