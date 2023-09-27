
model_functions = [
    ## Reminder functions
    {
        "name": "control_mplayer",
        "description": "send commands to the mplayer -slave -idle instance to do what the user want to do like pausing the song, loading another song, lowering the volume, skipping the song, etc",
        "parameters": {
            "type": "object",
            "properties": {
                "command":{
                    "type": "string",
                    "description": "the command to send to mplayer"
                },
            },
            "required": ["command",],
        },
    },
]
def function_caller(chatbot, f_name, f_args):
    if f_name == 'control_mplayer':
        print(f_name, f_args)
        command = f_args['command']
        print('command', command)
        chatbot.player.stdin.write(command.encode() + b'\n')
        chatbot.player.stdin.flush()
        return 'did soemthing'
