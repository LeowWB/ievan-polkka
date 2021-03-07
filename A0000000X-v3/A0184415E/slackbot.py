'''
    NUS CS4248 Assignment 1 - Objectives 1-3 Driver Code

    Classes Message, Echo, and helper functions for Slackbot
'''
from slack_sdk.rtm import RTMClient
import certifi
import ssl as ssl_lib
import re
from datetime import datetime
import json
import traceback
from obj1_tokenizer import Tokenizer
from obj2_weather import Weather
from obj3_ngram_lm import NgramLM

class Echo:

    def echo(self,text: str):
        ''' Echoes the text sent in '''
        reply = "You said: {}".format(text)
        return reply

class Message:

    def __init__(self, ts, username, text):
        self.ts = ts
        self.username = username
        self.text = text

    def toString(self):
        return f"Timestamp: {self.ts}, Username: {self.username}, Text: {self.text}"

    def toDict(self):
        data = {}
        data['Timestamp'] = self.ts
        data['Username'] = self.username
        data['Text'] = self.text
        return data

# List to keep track of messages sent and received
conversation = []

# TODO Make these whatever you want.
USERNAME = "Dude"
USER_EMOJI = ":sunglasses:"

# TODO Copy your Bot User OAuth-Access Token and paste it here
SLACK_TOKEN = "xoxb-1675623418278-1667643412839-w8MbaEYgfWitufxxMSJNH4Xj"

# You'll need to modify the code to call the functions that
# you've created in the rest of the exercises.
def make_message(user_input):
    ''' Driver function - Parses the user_input, calls the appropriate classes and functions
    and returns the output to the make_message() function

    Example input: user_input = "OBJ0 echo_text=Hi there"
    '''  

    # To stop the bot, simply enter the 'EXIT' command
    if user_input == 'EXIT':
        rtm_client.stop()
        with open('./conversation.json', 'w') as f:
            json.dump(conversation, f)
        return
  
    # Regex matching and calling appropriate classes and functions
    pattern_dict = {
        "OBJ0":r"OBJ0 echo_text=(?P<echo_text>.*)",
        "OBJ1":r"OBJ1 path=(?P<path>.*) n_top_words=(?P<n_top_words>\d+) lowercase=(?P<lowercase>YES|NO) stopwords=(?P<stopwords>YES|NO)",
        "OBJ2":r"OBJ2 (?P<input_text>.*)",
        "OBJ3":r"OBJ3 path=(?P<path>.*) smooth=(?P<smooth>add-k|add-k-interpolate) n_gram=(?P<n_gram>\d) k=(?P<k>\d+(?:\.\d+)?) text=(?P<text>[^~]*)~ next_word=(?P<next_word>.*) length=(?P<length>\d+)",
    }

    for key in pattern_dict.keys():
        match = re.match(pattern_dict[key], user_input)
        if match:
            # Dictionary with key as argument name and value as argument value
            commands_dict = match.groupdict()
            if key == "OBJ0":
                print("[SUCCESS] Matched objective 0")
                echo = Echo()
                reply = echo.echo(commands_dict['echo_text'])
                break

            elif key == "OBJ1":
                print("[SUCCESS] Matched objective 1")
                path = commands_dict['path']
                n_top_words = int(commands_dict['n_top_words'])
                lowercase = (commands_dict['lowercase'] == 'YES')
                stopwords = (commands_dict['stopwords'] == 'YES')
                print(f'finished parsing command {path} {n_top_words} {lowercase} {stopwords}')

                try:
                    tokenizer = Tokenizer(path, lowercase=lowercase)
                    print("made tokenizer")
                    if stopwords:
                        tokenizer.remove_stopwords()
                    print("stopwords gone")
                    reply = str(tokenizer.get_frequent_words(n_top_words))
                    print("got a reply")
                    print(reply)
                    print('plotting freq')
                    tokenizer.plot_word_frequency()
                except:
                    traceback.print_exc()

                break

            elif key == "OBJ2":
                print("[SUCCESS] Matched objective 2")
                input_text = commands_dict['input_text']
                print('finished parsing command')

                try:
                    weather = Weather('')
                    reply = weather.weather(input_text)
                    print(reply)
                    print("got a reply")
                except:
                    traceback.print_exc

                break
            
            elif key == "OBJ3":
                print("[SUCCESS] Matched objective 3")
                path = commands_dict['path']
                n_gram = int(commands_dict['n_gram'])
                k = float(commands_dict['k'])
                text = str(commands_dict['text'])
                next_word = str(commands_dict['next_word'])
                length = int(commands_dict['length'])
                
                if commands_dict['smooth'].lower() == 'add-k':
                    interpolate = False
                else:
                    interpolate = True
                    
                print(f'finished parsing command {path} {n_gram} {k} {text} {next_word} {length} {interpolate}')

                try:
                    ngramlm = NgramLM(n_gram, k, interpolation=interpolate)
                    ngramlm.read_file(path)
                    reply = "Generated Word: " + ngramlm.generate_word(text)
                    print('generated word')
                    reply += "\nProbability of next word: " + str(ngramlm.get_next_word_probability(text, next_word))
                    print('got probability')
                    reply += "\nPerplexity: " + str(ngramlm.perplexity(text))
                    print('got perplexity')
                    reply += "\nGenerated Text: " + ngramlm.generate_text(length)
                    print("got a reply")
                    print(reply)
                except:
                    traceback.print_exc()

                break
        
            else:
                print("[ERROR] Did not match any commands!")

    return reply


def do_respond(web_client, channel, text):
    # Post the message in Slack
    web_client.chat_postMessage(channel=channel,
                                username=USERNAME,
                                icon_emoji=USER_EMOJI,
                                text=make_message(text))

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the update_share callback to the 'message' event.
@RTMClient.run_on(event="message")

def message(**payload):
    """
    Call do_respond() with the appropriate information for all incoming
    direct messages to our bot.
    """
    web_client = payload["web_client"]

    # Getting information from the response
    data = payload["data"]
    channel_id = data.get("channel")
    text = data.get("text")
    subtype = data.get("subtype")
    ts = data['ts']
    user = data.get('username') if not data.get('user') else data.get('user')

    # Creating a Converstion object
    message = Message(ts, user, text)

    # Appending the converstion attributes to the logs
    conversation.append(message.toDict())

    if subtype == 'bot_message': return

    do_respond(web_client, channel_id, text)

# You probably won't need to modify any of the code below.
# It is used to appropriately install the bot.
def main():
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    # Real-time messaging client with Slack
    global rtm_client
    rtm_client = RTMClient(token=SLACK_TOKEN, ssl=ssl_context)
    try:
        print("[SUCCESS] Your bot is running!")
        rtm_client.start()
    except:
        print("[ERROR] Your bot is not running.")

if __name__ == "__main__":
    main()
