from chatbot import ChatBot, MusicBot

chatbot = MusicBot()
while True:
  try:
    responses = chatbot.get_chatbot_response(input('> '))
    for res in responses:
      print(res)
  except Exception as e:
    print(f'there was an error', e)