from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

# choose set to train from
path = './assets/train/data/'
training_set = 'training_data'

# create and train bot
bot = ChatBot(
    "List Bot",
    database="./assets/bots/database/list.db",
    trainer="chatterbot.trainers.ListTrainer"
)

for files in os.listdir(path + training_set + '/'):
    data = open(path + training_set + '/' + files, 'r').readlines()
    bot.train(data)
