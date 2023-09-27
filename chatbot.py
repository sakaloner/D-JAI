import os
import openai
import json
from chatbot_functions.all import model_functions, function_caller
from chatbot_functions import test 

import logging
logging.basicConfig(
  filename='app.log',
  filemode='w',
  format='%(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)

openai.api_key = os.getenv("OPENAI_API_KEY")

first_prompt= """
you a dj ai, your job is to search for music, give recommendations, play music, 
and stop music with the functions you have at your disposal.  
you have the ability to play music by sending functions to a music player.
"""

class ChatBot:
  def __init__(self, interaction_history=None):
    self.model_functions = model_functions
    self.model_type = 'gpt-3.5-turbo-0613'
    self.interaction_history = [
      {"role":"system", "content":first_prompt},
    ]
    if interaction_history:
      self.interaction_history += interaction_history

  def call_model(self, history=None, function_calling="auto"):
    messages = self.interaction_history if history == None else history
    completion = openai.ChatCompletion.create(
      model=self.model_type,
      messages=messages,
      functions=self.model_functions,
      function_call=function_calling
    )
    return completion["choices"][0]["message"]

  def get_chatbot_response(self, message):
    self.interaction_history.append({"role": "user", "content": message})
    response = self.call_model()
    logging.info(json.dumps(response))

    ## response is a function
    if response.get("function_call"):
        f_name = response["function_call"]["name"]
        yield f'waiting for the function {f_name} to finish'

        f_args = json.loads(response["function_call"]["arguments"])
        sys_prompt = function_caller(self, f_name, f_args)
        self.interaction_history.append({"role":"system","content":sys_prompt})
        ## stop the model from getting stuck in a infinite function call
        new_res = self.call_model(function_calling="none")

        self.interaction_history.append(new_res)
        logging.info(json.dumps(self.interaction_history, indent=4))
        yield new_res.content

    ## response is not a function
    else:
        response = response["content"]
        self.interaction_history.append({"role":"assistant", "content":response})
        logging.info(json.dumps(self.interaction_history))
        yield response

import threading
import subprocess
class MusicBot(ChatBot):
  def __init__(self, interaction_history=None):
    super().__init__(interaction_history)
    self.model_functions = model_functions 
    self.playlist = False 
    self.player = subprocess.Popen(['mplayer', '-slave', '-idle',], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Start two threads, to continuously read from stdout and stderr
    threading.Thread(target=self._read_stream, args=(self.player.stdout,)).start()
    threading.Thread(target=self._read_stream, args=(self.player.stderr,)).start()

  def _read_stream(self, stream):
    while True:
      line = stream.readline()
      if line == b'':  # End of file
          break
      #print(line.decode().strip()) 



  