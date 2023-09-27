"""
##(search_song('my favourite things'))
import subprocess

# Start the player
player = subprocess.Popen(['mpg123', '-R'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Load a playlist
player.stdin.write(b'LOADLIST ./playlist.pls\n')
player.stdin.flush()

input('hello')
exit()
import subprocess
global player
music_file = './music/test - test.mp3'

def play_music():
  player = subprocess.Popen(['mpg123', '-R'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  player.stdin.write(b'L ' + music_file.encode() + b'\n')
  player.stdin.flush()

def pause_music():
  player.stdin.write(b'P\n')
  player.stdin.flush()

def stop_music():
  player.stdin.write(b'S\n')
  player.stdin.flush()


if __name__ == '__main__':
  
  input('close with any pressing')
"""