import subprocess
from tkinter import *
from tkinter import filedialog
import threading

class MusicPlayer:

    def __init__(self, window ):
        window.geometry('400x150'); 
        window.title('Iris MP3 Player'); 
        window.resizable(0,0)

        # Open file
        self.load = Button(window, text = 'Load',  width = 10, font = ('Times', 10), command = self.load_file)
        self.load.place(x=0,y=20);

        # Play file
        self.play = Button(window, text = 'Play',  width = 10, font = ('Times', 10), command = self.play_music)
        self.play.place(x=100,y=20);

        # Pause file
        self.pause = Button(window,text = 'Pause',  width = 10, font = ('Times', 10), command = self.pause_music)
        self.pause.place(x=200,y=20);

        # Stop file
        self.stop = Button(window ,text = 'Stop',  width = 10, font = ('Times', 10), command = self.stop_music)
        self.stop.place(x=300,y=20);

        self.music_file = False
        self.playing_state = False

    def load_file(self):
        self.music_file = filedialog.askopenfilename()

    def play_music(self):
        if self.music_file:
            self.player = subprocess.Popen(['mpg123', '-R'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.player.stdin.write(b'L ' + self.music_file.encode() + b'\n')
            self.player.stdin.flush()
            self.playing_state = True

    def pause_music(self):
        if self.playing_state:
            self.player.stdin.write(b'P\n')
            self.player.stdin.flush()
            self.playing_state = False

    def stop_music(self):
        if self.playing_state:
            self.player.stdin.write(b'S\n')
            self.player.stdin.flush()
            self.playing_state = False

def chatbot(music_player):
    while True:
        command = input('Enter command: ')
        if command == 'play':
            music_player.play_music()
        elif command == 'pause':
            music_player.pause_music()
        elif command == 'stop':
            music_player.stop_music()

# root = Tk()
# music_player = MusicPlayer(root)

# chatbot_thread = threading.Thread(target=chatbot, args=(music_player,))
# chatbot_thread.start()

# root.mainloop()