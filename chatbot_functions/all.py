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
]

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
        search_play_song(chatbot.player, song_name)
        return f'the song {song_name} is now playing. tell the user the song is playing'

