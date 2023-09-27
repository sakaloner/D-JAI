# from pprint import pprint
# from chatbot import ChatBot




# from tkinter import Tk
# import threading
# from ui import MusicPlayer
from chatbot import ChatBot, MusicBot

# # Initialize the tkinter root UI
# root = Tk()

# # Pass the tkinter root UI to MusicPlayer
# music_player = MusicPlayer(root)

# # Initialize the ChatBot
# chat_bot = ChatBot(music_player)


def general_test():
  chatbot = MusicBot()
  while True:
    try:
      responses = chatbot.get_chatbot_response(input('>'))
      for res in responses:
        print(res)
    except Exception as e:
      print(f'there was an error', e)

def testing_video_download():
  message=""" 
  yo!!! i want to download this fire music, with the tags,
  hip hop melodic insipired upbeat maniac kanye energy religious https://www.youtube.com/watch?v=qAsHVwl-MU4&list=RDMM&index=10
    """
  interaction_history = {"role":"system", "content":message},
  chatbot = ChatBot(interaction_history=interaction_history)
  responses = chatbot.get_chatbot_response(message=message)
  for res in responses :
    print(res)

def test_recs():
  message=""" 
  recommend me italian music
  """
  interaction_history = {"role":"system", "content":message},
  chatbot = ChatBot(interaction_history=interaction_history)
  responses = chatbot.get_chatbot_response(message=message)
  for res in responses :
    print(res)

def test_search_and_play():
  message="""play the song dope lemon salt and pepper
  """
  interaction_history = {"role":"system", "content":message},
  chatbot = MusicBot(interaction_history=interaction_history)
  responses = chatbot.get_chatbot_response(message=message)
  for res in responses :
    print(res)

if __name__=="__main__":
  general_test()
  #testing_video_download()
  #test_recs()
  #test_search_and_play()
