#************************************************************
#
#   chatbot.py  
#   
#   author      pxl
#   since       04/16/2018
#   update      04/22/2018
#
#************************************************************
import os
import sys
import time
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from chatterbot import ChatBot

#************************************************************
#
#   initialize
#
#************************************************************
# get path from os
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# set up Flask and socketio
app = Flask(__name__)
app.config['SECRET_KEY'] = 'io7xlerfpegey8uc531dbygi'
socketio = SocketIO(app)

# load chatterbot from database
list_bot = ChatBot(
  "List Bot",
  database="./bots/database/list.db"
)

#************************************************************
#
#   record converations
#
#************************************************************
def logConversation(msg):
  orig_stdout = sys.stdout
  f = open('conversation.yml', 'a')
  sys.stdout = f
  print('- - ', msg)
  sys.stdout = orig_stdout
  f.close()

#************************************************************
#
#   debugging
#
#************************************************************
def messageRecived():
  print('message was received!!!')

#************************************************************
#
#   home page
#
#************************************************************
@app.route('/')
def hello():
  j2_env = Environment(loader = FileSystemLoader(THIS_DIR), trim_blocks = True)
  return j2_env.get_template('templates/home.html').render(response = 'hello')

#************************************************************
#
#   response
#
#************************************************************
@socketio.on('response')
def response_event(json):
  # check if user or bot response
  if 'bot' in json:
    bot_response = eval(str(json['bot']))
  else:
    bot_response = False

  # replace user response with bot response
  if(bot_response):
    message = json['message']
    json['message'] = str(list_bot.get_response(message));

  # log response for future training
  if 'message' in json:
    if json['message'] != '':
      message = json['message']
      logConversation(message)

  # output response
  socketio.emit('my response', json, callback = messageRecived)

#************************************************************
#
#   main driver
#
#************************************************************
if __name__ == '__main__':
  socketio.run(app, host = '0.0.0.0', port = 8000, debug = True)
